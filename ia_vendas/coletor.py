"""Analisa o HTML de UMA página e devolve um dicionário com o que importa para vendas.

Não busca nada na internet: recebe o HTML pronto. Assim dá para testar com arquivos locais.
Tudo o que sai daqui é estatuto I (inferido do HTML); nada é verificado em fonte oficial.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

# Medição de terceiros: nome -> padrão procurado nos <script> (endereço ou código).
TRACKERS = [
    ("Google Analytics / Tag Manager", r"googletagmanager\.com|google-analytics\.com|\bgtag\(|\bga\(\s*['\"]create"),
    ("Meta Pixel", r"connect\.facebook\.net|\bfbq\("),
    ("Microsoft Clarity", r"clarity\.ms|\bclarity\("),
    ("Microsoft Ads (UET)", r"bat\.bing\.com|\buetq\b"),
    ("Hotjar", r"hotjar\.com|\bhj\("),
    ("Plausible", r"plausible\.io"),
    ("Matomo", r"matomo|piwik"),
    ("TikTok Pixel", r"analytics\.tiktok\.com|\bttq\."),
    ("LinkedIn Insight", r"snap\.licdn\.com|_linkedin_partner_id"),
    ("X (Twitter) Pixel", r"static\.ads-twitter\.com|\btwq\("),
]
# Dica de medição própria (sem cookies de terceiros): envio de eventos ao próprio servidor.
MEDICAO_PROPRIA = re.compile(r"sendBeacon|/api/(evento|visita|track|medir|analytics)|/medir\.js|\bmedir\.js", re.I)
PRECO = re.compile(r"R\$\s*\d")
PROVA_SOCIAL = re.compile(r"depoimento|testemunho|avalia(ç|c)(ão|ões|ao|oes)\b|estrelas|clientes dizem|o que dizem|leitores dizem", re.I)
PRIVACIDADE = re.compile(r"privacidade|privacy|lgpd", re.I)
CLASSES_CTA = ("btn", "button", "cta")


def dominio_base(host: str) -> str:
    """'enquanto.escoladecriacaoderealidade.com.br' -> 'escoladecriacaoderealidade.com.br'."""
    host = (host or "").lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    partes = host.split(".")
    if len(partes) >= 3 and partes[-2] in ("com", "org", "net", "gov", "edu") and len(partes[-1]) == 2:
        return ".".join(partes[-3:])
    return ".".join(partes[-2:])


def _sem_www(host: str) -> str:
    host = (host or "").lower().split(":")[0]
    return host[4:] if host.startswith("www.") else host


def tipo_link(href: str, host_base: str) -> str:
    """interno (mesmo site), subdominio (mesmo domínio, outro endereço), externo ou contato."""
    p = urlparse(href)
    if p.scheme in ("mailto", "tel"):
        return "contato"
    host = _sem_www(p.netloc)
    if not host or host == _sem_www(host_base):
        return "interno"
    if dominio_base(host) == dominio_base(host_base):
        return "subdominio"
    return "externo"


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self._em_title = False
        self.meta_nome: dict[str, str] = {}
        self.meta_prop: dict[str, str] = {}
        self.canonical = None
        self.jsonld: list[str] = []
        self.scripts_src: list[str] = []
        self.scripts_inline: list[str] = []
        self._script: tuple[str, list[str]] | None = None
        self.titulos: dict[str, list[str]] = {"h1": [], "h2": [], "h3": []}
        self._h: tuple[str, list[str]] | None = None
        self.ancoras: list[dict] = []
        self._a: dict | None = None
        self.forms: list[dict] = []
        self._form: dict | None = None
        self.imgs = 0
        self.imgs_sem_alt = 0
        self.texto: list[str] = []
        self._ignorar = 0  # dentro de <script> ou <style>

    # --- abertura de tags
    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        elif tag == "title":
            self._em_title = True
        elif tag == "meta":
            if a.get("name"):
                self.meta_nome[a["name"].lower()] = a.get("content", "")
            if a.get("property"):
                self.meta_prop[a["property"].lower()] = a.get("content", "")
        elif tag == "link":
            if "canonical" in a.get("rel", "").lower().split():
                self.canonical = a.get("href")
        elif tag == "script":
            self._ignorar += 1
            if a.get("src"):
                self.scripts_src.append(a["src"])
            self._script = (a.get("type", "").lower(), [])
        elif tag == "style":
            self._ignorar += 1
        elif tag in self.titulos:
            self._h = (tag, [])
        elif tag == "a":
            self._fechar_ancora()   # um <a> novo fecha o anterior que ficou sem </a>
            self._a = {"href": a.get("href", ""), "classe": a.get("class", ""), "role": a.get("role", ""), "texto": []}
        elif tag == "form":
            self._form = {"campos": []}
        elif tag in ("input", "select", "textarea") and self._form is not None:
            tipo = a.get("type", "text").lower() if tag == "input" else tag
            self._form["campos"].append(tipo)
        elif tag == "img":
            self.imgs += 1
            if "alt" not in a:
                self.imgs_sem_alt += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in ("script", "style"):
            self.handle_endtag(tag)

    # --- fechamento de tags
    def handle_endtag(self, tag):
        if tag == "title":
            self._em_title = False
        elif tag == "script":
            self._ignorar = max(0, self._ignorar - 1)
            if self._script is not None:
                tipo, buf = self._script
                texto = "".join(buf)
                if "ld+json" in tipo:
                    self.jsonld.append(texto)
                elif texto.strip():
                    self.scripts_inline.append(texto)
                self._script = None
        elif tag == "style":
            self._ignorar = max(0, self._ignorar - 1)
        elif tag in self.titulos and self._h and self._h[0] == tag:
            self.titulos[tag].append(" ".join("".join(self._h[1]).split()))
            self._h = None
        elif tag == "a" and self._a is not None:
            self._fechar_ancora()
        elif tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None

    def _fechar_ancora(self):
        if self._a is not None:
            self._a["texto"] = " ".join("".join(self._a["texto"]).split())
            self.ancoras.append(self._a)
            self._a = None

    def finalizar(self):
        """Fecha o que ficou aberto no fim do arquivo (HTML da vida real nem sempre fecha as tags)."""
        self._fechar_ancora()
        if self._h:
            self.titulos[self._h[0]].append(" ".join("".join(self._h[1]).split()))
            self._h = None
        if self._form is not None:
            self.forms.append(self._form)
            self._form = None

    def handle_data(self, data):
        if self._em_title:
            self.title += data
        if self._script is not None:
            self._script[1].append(data)
            return
        if self._ignorar:
            return
        self.texto.append(data)
        if self._h is not None:
            self._h[1].append(data)
        if self._a is not None:
            self._a["texto"].append(data)


def _tipos_jsonld(objeto, acc: list[str]) -> None:
    if isinstance(objeto, list):
        for o in objeto:
            _tipos_jsonld(o, acc)
    elif isinstance(objeto, dict):
        t = objeto.get("@type")
        if isinstance(t, str):
            acc.append(t)
        elif isinstance(t, list):
            acc.extend(str(x) for x in t)
        if "@graph" in objeto:
            _tipos_jsonld(objeto["@graph"], acc)


def analisar_html(html: str, url: str) -> dict:
    p = _Parser()
    p.feed(html)
    p.close()
    p.finalizar()
    host_base = urlparse(url).netloc

    # Dados estruturados
    tipos: list[str] = []
    invalidos = 0
    for bruto in p.jsonld:
        try:
            _tipos_jsonld(json.loads(bruto), tipos)
        except ValueError:
            invalidos += 1

    # Links e botões de ação
    links, ctas = [], []
    for a in p.ancoras:
        href = (a["href"] or "").strip()
        if not href or href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        absoluto = urljoin(url, href).split("#")[0]
        item = {"href": absoluto, "texto": a["texto"][:80], "tipo": tipo_link(absoluto, host_base)}
        links.append(item)
        classes = a["classe"].lower()
        if any(c in classes for c in CLASSES_CTA) or a["role"].lower() == "button":
            ctas.append(item)

    # Medição
    corpo_scripts = " ".join(p.scripts_inline + p.scripts_src)
    trackers = [nome for nome, padrao in TRACKERS if re.search(padrao, corpo_scripts, re.I)]
    texto = " ".join(" ".join(p.texto).split())

    return {
        "url": url,
        "titulo": p.title.strip() or None,
        "descricao": p.meta_nome.get("description") or None,
        "canonical": p.canonical,
        "lang": p.lang,
        "robots_meta": p.meta_nome.get("robots"),
        "og": {k: v for k, v in p.meta_prop.items() if k.startswith("og:")},
        "twitter": {k: v for k, v in p.meta_nome.items() if k.startswith("twitter:")},
        "jsonld": {"blocos": len(p.jsonld), "tipos": sorted(set(tipos)), "invalidos": invalidos},
        "titulos": {k: v[:12] for k, v in p.titulos.items()},
        "n_h1": len(p.titulos["h1"]),
        "links": links,
        "ctas": ctas,
        "formularios": [{"campos": f["campos"], "tem_email": "email" in f["campos"]} for f in p.forms],
        "imagens": {"total": p.imgs, "sem_alt": p.imgs_sem_alt},
        "scripts_externos": sorted({s for s in p.scripts_src}),
        "trackers": trackers,
        "medicao_propria_dica": bool(MEDICAO_PROPRIA.search(corpo_scripts)),
        "tem_preco": bool(PRECO.search(texto)),
        "tem_prova_social": bool(PROVA_SOCIAL.search(texto)),
        "tem_link_privacidade": any(PRIVACIDADE.search(l["href"]) or PRIVACIDADE.search(l["texto"]) for l in links),
        "tamanho_texto": len(texto),
    }
