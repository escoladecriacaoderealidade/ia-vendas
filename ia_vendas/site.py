"""Percorre um site: robots.txt, sitemap, llms.txt e páginas. Devolve um dicionário com o resumo.

"Buscar" é uma função que recebe um endereço e devolve (status, tipo_de_conteudo, corpo).
Status 0 = falha de rede; 999 = bloqueado pelo robots.txt do site (não insistimos).
Dois buscadores prontos:
  - criar_fetch_http: pela internet, com robots.txt respeitado, pausa entre pedidos e limite de tamanho;
  - criar_fetch_dir: de uma pasta local (o repositório de um site estático), útil para testar sem rede.
"""
from __future__ import annotations

import re
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

from .coletor import analisar_html, dominio_base

Buscar = Callable[[str], "tuple[int, str, str]"]

USER_AGENT = "IAVendasBot/0.1 (+https://github.com/escoladecriacaoderealidade/ia-vendas)"
BLOQUEADO_POR_ROBOTS = 999
ROBOS_DE_IA = ("GPTBot", "ClaudeBot", "PerplexityBot", "OAI-SearchBot", "Google-Extended", "CCBot", "Bingbot", "Googlebot")


# ---------------------------------------------------------------- buscadores
def criar_fetch_http(user_agent: str = USER_AGENT, timeout: float = 10.0, intervalo: float = 1.0,
                     respeitar_robots: bool = True, limite_bytes: int = 2_000_000) -> Buscar:
    robots: dict[str, RobotFileParser] = {}
    ultimo = [0.0]

    def _pausa():
        espera = intervalo - (time.monotonic() - ultimo[0])
        if espera > 0:
            time.sleep(espera)
        ultimo[0] = time.monotonic()

    def _pedido(url: str):
        return Request(url, headers={"User-Agent": user_agent,
                                     "Accept": "text/html,application/xhtml+xml,application/xml,text/plain;q=0.9,*/*;q=0.5"})

    def _permitido(url: str) -> bool:
        p = urlparse(url)
        origem = f"{p.scheme}://{p.netloc}"
        if origem not in robots:
            rp = RobotFileParser()
            _pausa()
            try:
                with urlopen(_pedido(origem + "/robots.txt"), timeout=timeout) as r:
                    rp.parse(r.read(limite_bytes).decode("utf-8", "replace").splitlines())
            except HTTPError as e:
                if e.code in (401, 403):
                    rp.disallow_all = True
                else:
                    rp.allow_all = True
            except Exception:
                rp.allow_all = True
            robots[origem] = rp
        return robots[origem].can_fetch(user_agent, url)

    def buscar(url: str):
        if respeitar_robots and not url.endswith("/robots.txt") and not _permitido(url):
            return BLOQUEADO_POR_ROBOTS, "", ""
        _pausa()
        try:
            with urlopen(_pedido(url), timeout=timeout) as r:
                tipo = r.headers.get("Content-Type", "")
                if not re.search(r"text/|xml|json", tipo, re.I):
                    return r.status, tipo, ""
                bruto = r.read(limite_bytes + 1)[:limite_bytes]
                m = re.search(r"charset=([\w-]+)", tipo, re.I)
                try:
                    return r.status, tipo, bruto.decode(m.group(1) if m else "utf-8", "replace")
                except LookupError:
                    return r.status, tipo, bruto.decode("utf-8", "replace")
        except HTTPError as e:
            return e.code, "", ""
        except Exception:
            return 0, "", ""

    return buscar


def criar_fetch_dir(raiz: "str | Path | list[str | Path]") -> Buscar:
    """Serve os arquivos de uma ou mais pastas como se fossem o site (para analisar um site estático sem rede).

    Com várias pastas, vale a primeira que tiver o arquivo (sobreposição). Serve para sites montados em camadas,
    como o Enquanto Estuda, cuja home vem de uma pasta e os guias de outra.
    """
    bases = [Path(r).resolve() for r in (raiz if isinstance(raiz, (list, tuple)) else [raiz])]
    tipos = {".html": "text/html", ".xml": "application/xml", ".txt": "text/plain", ".json": "application/json"}

    def buscar(url: str):
        caminho = urlparse(url).path or "/"
        rel = caminho.lstrip("/")
        for base in bases:
            candidatos = [base / rel / "index.html"] if (caminho.endswith("/") or not rel) else [base / rel, base / rel / "index.html"]
            for c in candidatos:
                try:
                    c = c.resolve()
                    if (base in c.parents or c == base) and c.is_file():
                        return 200, tipos.get(c.suffix.lower(), "text/plain"), c.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
        return 404, "", ""

    return buscar


# ---------------------------------------------------------------- robots e sitemap
def _analisar_robots(resposta) -> dict:
    status, _, corpo = resposta
    if status != 200:
        return {"existe": False, "status": status, "agentes": [], "ia_bloqueada": [], "bloqueia_tudo": False, "sitemaps": []}
    agentes: list[str] = []
    bloqueios: dict[str, list[str]] = {}
    sitemaps: list[str] = []
    atuais: list[str] = []
    ultima_era_agente = False
    for linha in corpo.splitlines():
        linha = linha.split("#")[0].strip()
        if ":" not in linha:
            continue
        chave, valor = (s.strip() for s in linha.split(":", 1))
        chave = chave.lower()
        if chave == "user-agent":
            if not ultima_era_agente:
                atuais = []
            atuais.append(valor)
            if valor not in agentes:
                agentes.append(valor)
            ultima_era_agente = True
            continue
        ultima_era_agente = False
        if chave == "disallow" and valor == "/":
            for a in atuais:
                bloqueios.setdefault(a, []).append(valor)
        elif chave == "sitemap":
            sitemaps.append(valor)
    minusculos = {a.lower(): a for a in bloqueios}
    ia_bloqueada = [r for r in ROBOS_DE_IA if r.lower() in minusculos]
    return {"existe": True, "status": 200, "agentes": agentes, "ia_bloqueada": ia_bloqueada,
            "bloqueia_tudo": "*" in bloqueios, "sitemaps": sitemaps}


def _ler_sitemaps(origem: str, buscar: Buscar, declarados: list[str], max_arquivos: int = 6) -> tuple[list[str], list[str]]:
    fila = deque(declarados or [origem + "/sitemap.xml"])
    lidos, urls = [], []
    while fila and len(lidos) < max_arquivos:
        mapa = fila.popleft()
        if mapa in lidos:
            continue
        status, _, corpo = buscar(mapa)
        if status != 200:
            continue
        lidos.append(mapa)
        locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", corpo, re.S | re.I)
        if "<sitemapindex" in corpo.lower():
            fila.extend(locs)
        else:
            urls.extend(locs)
    base = dominio_base(urlparse(origem).netloc)
    vistos, saida = set(), []
    for u in urls:
        u = u.split("#")[0]
        if dominio_base(urlparse(u).netloc) == base and u not in vistos:
            vistos.add(u)
            saida.append(u)
    return saida, lidos


# ---------------------------------------------------------------- coleta
def _eh_html(tipo: str, corpo: str) -> bool:
    return "html" in tipo.lower() or corpo.lstrip()[:15].lower().startswith(("<!doctype html", "<html"))


def coletar_site(base_url: str, buscar: Buscar, max_paginas: int = 60) -> dict:
    p = urlparse(base_url)
    origem = f"{p.scheme}://{p.netloc}"
    home = origem + (p.path if p.path else "/")

    robots = _analisar_robots(buscar(origem + "/robots.txt"))
    llms = buscar(origem + "/llms.txt")[0] == 200
    urls_mapa, mapas_lidos = _ler_sitemaps(origem, buscar, robots["sitemaps"])

    unicas = list(dict.fromkeys([home] + urls_mapa))   # a home costuma estar também no sitemap: ler uma vez só
    fila = deque(unicas)
    descobrir_por_links = not urls_mapa
    vistos = set(unicas)
    paginas: list[dict] = []
    truncado = False
    while fila:
        if len(paginas) >= max_paginas:
            truncado = True
            break
        url = fila.popleft()
        status, tipo, corpo = buscar(url)
        if status == 200 and corpo and _eh_html(tipo, corpo):
            analise = analisar_html(corpo, url)
            analise["status"] = status
            paginas.append(analise)
            if descobrir_por_links:
                for l in analise["links"]:
                    if l["tipo"] == "interno" and l["href"] not in vistos and not re.search(r"\.(jpe?g|png|webp|gif|svg|pdf|zip|css|js)$", l["href"], re.I):
                        vistos.add(l["href"])
                        fila.append(l["href"])
        else:
            paginas.append({"url": url, "status": status})

    return {
        "base_url": base_url,
        "coletado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "robots": robots,
        "llms_txt": llms,
        "sitemap": {"arquivos": mapas_lidos, "urls": len(urls_mapa)},
        "paginas": paginas,
        "resumo": resumir(paginas, origem),
        "limites": {"max_paginas": max_paginas, "paginas_lidas": len(paginas), "truncado": truncado},
    }


def resumir(paginas: list[dict], origem: str) -> dict:
    ok = [p for p in paginas if p.get("status") == 200 and "titulo" in p]
    host_base = urlparse(origem).netloc
    contar = lambda cond: sum(1 for p in ok if cond(p))  # noqa: E731

    tipos: dict[str, int] = {}
    trackers: dict[str, int] = {}
    destinos: dict[str, dict] = {}
    ctas: dict[tuple[str, str], int] = {}
    for p in ok:
        for t in p["jsonld"]["tipos"]:
            tipos[t] = tipos.get(t, 0) + 1
        for t in p["trackers"]:
            trackers[t] = trackers.get(t, 0) + 1
        hosts_da_pagina = set()
        for l in p["links"]:
            if l["tipo"] in ("subdominio", "externo"):
                h = urlparse(l["href"]).netloc.lower()
                d = destinos.setdefault(h, {"tipo": l["tipo"], "links": 0, "paginas": 0})
                d["links"] += 1
                hosts_da_pagina.add(h)
        for h in hosts_da_pagina:
            destinos[h]["paginas"] += 1
        for c in p["ctas"]:
            chave = (c["texto"], c["href"])
            ctas[chave] = ctas.get(chave, 0) + 1
    top_ctas = [{"texto": t, "href": h, "vezes": n} for (t, h), n in sorted(ctas.items(), key=lambda x: -x[1])[:10]]

    return {
        "paginas_lidas": len(ok),
        "paginas_com_erro": len(paginas) - len(ok),
        "sem_titulo": contar(lambda p: not p["titulo"]),
        "sem_descricao": contar(lambda p: not p["descricao"]),
        "sem_canonical": contar(lambda p: not p["canonical"]),
        "sem_og_image": contar(lambda p: "og:image" not in p["og"]),
        "sem_twitter_card": contar(lambda p: "twitter:card" not in p["twitter"]),
        "sem_jsonld": contar(lambda p: p["jsonld"]["blocos"] == 0),
        "jsonld_invalidos": sum(p["jsonld"]["invalidos"] for p in ok),
        "jsonld_tipos": tipos,
        "paginas_h1_multiplos": contar(lambda p: p["n_h1"] > 1),
        "paginas_sem_h1": contar(lambda p: p["n_h1"] == 0),
        "imagens_total": sum(p["imagens"]["total"] for p in ok),
        "imagens_sem_alt": sum(p["imagens"]["sem_alt"] for p in ok),
        "trackers": trackers,
        "paginas_com_medicao_propria": contar(lambda p: p["medicao_propria_dica"]),
        "paginas_com_preco": contar(lambda p: p["tem_preco"]),
        "paginas_com_prova_social": contar(lambda p: p["tem_prova_social"]),
        "paginas_com_link_privacidade": contar(lambda p: p["tem_link_privacidade"]),
        "formularios": sum(len(p["formularios"]) for p in ok),
        "formularios_com_email": sum(1 for p in ok for f in p["formularios"] if f["tem_email"]),
        "destinos_fora_do_host": destinos,
        "ctas_principais": top_ctas,
    }
