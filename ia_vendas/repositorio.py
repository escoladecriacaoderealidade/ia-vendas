"""Lê uma pasta de projeto (um repositório clonado) e resume o que importa para vendas.

Procura: regras e decisões do dono (CLAUDE.md etc.), o que já existe de SEO, medição própria e de terceiros,
política de privacidade, implantação e pendências. Só lê; nunca altera nada.
Tudo o que sai daqui é estatuto I (inferido do código). As linhas de regras saem como "D?": candidatas a decisão
do cliente, que uma pessoa confirma.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

ARQUIVOS_DE_REGRAS = ("CLAUDE.md", "AGENTS.md", "CONTEXTO.md", "README.md")
# "_cache" e ".cache" guardam cópias de páginas de OUTROS sites (ex.: súmulas do STF no Enquanto): o código de
# medição delas não é do cliente e gerava falso "Google Analytics" no relatório.
IGNORAR = {".git", "node_modules", ".venv", "venv", "__pycache__", ".vercel", "dist", "build", ".next", ".expo",
           "_cache", ".cache"}
EXT_TEXTO = {".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".py", ".json", ".md", ".txt", ".xml"}
EXT_CODIGO = {".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".py"}
LIMITE_ARQUIVO = 8_000_000   # o app do Enquanto é um único HTML de vários MB; pular arquivo grande esconderia a medição
LIMITE_ARQUIVOS = 5000

DECISAO = re.compile(r"\b(nunca|n[ãa]o\s+(copiar|colocar|prometer|mexer|alterar|usar|publicar|apagar|commitar|escrever|mostrar)|"
                     r"proibid[oa]|obrigat[óo]ri[oa]|decis[ãa]o|regra|sem\s+pre[çc]o)\b", re.I)
MEDICAO_TERCEIROS = {
    "Google Analytics / Tag Manager": r"googletagmanager\.com|google-analytics\.com|\bgtag\(",
    "Meta Pixel": r"connect\.facebook\.net|\bfbq\(",
    "Microsoft Clarity": r"clarity\.ms",
    "Hotjar": r"hotjar\.com",
}
MEDICAO_PROPRIA = {
    "envio de eventos (sendBeacon)": r"sendBeacon",
    "rota de eventos": r"/api/(evento|visita|track|medir|analytics)",
}
ANUNCIOS = re.compile(r"\b(gclid|gbraid|wbraid|msclkid|fbclid)\b")


def _arquivos(raiz: Path):
    n = 0
    for dirpath, dirnames, nomes in os.walk(raiz):
        dirnames[:] = [d for d in dirnames if d not in IGNORAR]
        for nome in nomes:
            n += 1
            if n > LIMITE_ARQUIVOS:
                return
            yield Path(dirpath) / nome


def _ler(caminho: Path) -> str | None:
    try:
        if caminho.stat().st_size > LIMITE_ARQUIVO:
            return None
        return caminho.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def ler_repositorio(caminho: str | Path) -> dict:
    raiz = Path(caminho).resolve()
    if not raiz.is_dir():
        raise FileNotFoundError(f"Pasta não encontrada: {raiz}")

    arquivos = list(_arquivos(raiz))
    rel = lambda p: p.relative_to(raiz).as_posix()  # noqa: E731

    # Regras e decisões do dono
    instrucoes, decisoes = [], []
    for nome in ARQUIVOS_DE_REGRAS:
        p = raiz / nome
        if p.is_file():
            texto = _ler(p) or ""
            instrucoes.append({"arquivo": nome, "tamanho": len(texto)})
            if nome == "README.md":
                continue
            for i, linha in enumerate(texto.splitlines(), 1):
                l = linha.strip()
                # Vale lista e parágrafo: "Não copiar preços para o site" costuma vir em texto corrido.
                if l and not l.startswith("#") and DECISAO.search(l) and len(decisoes) < 60:
                    decisoes.append({"arquivo": nome, "linha": i, "texto": l[:300], "estatuto": "D?"})

    # Estrutura
    pastas: dict[str, int] = {}
    extensoes: dict[str, int] = {}
    for p in arquivos:
        partes = p.relative_to(raiz).parts
        pastas[partes[0] if len(partes) > 1 else "(raiz)"] = pastas.get(partes[0] if len(partes) > 1 else "(raiz)", 0) + 1
        extensoes[p.suffix.lower() or "(sem)"] = extensoes.get(p.suffix.lower() or "(sem)", 0) + 1

    nomes = {p.name.lower(): p for p in arquivos}
    seo = {n: [rel(p) for p in arquivos if p.name.lower() == n][:3] for n in ("robots.txt", "sitemap.xml", "llms.txt")}

    # Varredura do código: dados estruturados, medição, anúncios
    jsonld = 0
    terceiros: dict[str, list[str]] = {}
    proprios: dict[str, list[str]] = {}
    reconhece_anuncios = False
    for p in arquivos:
        if p.suffix.lower() not in EXT_CODIGO:
            continue
        t = _ler(p)
        if not t:
            continue
        if "application/ld+json" in t or "ld+json" in t:
            jsonld += 1
        for nome, padrao in MEDICAO_TERCEIROS.items():
            if re.search(padrao, t, re.I):
                terceiros.setdefault(nome, []).append(rel(p))
        for nome, padrao in MEDICAO_PROPRIA.items():
            if re.search(padrao, t, re.I):
                proprios.setdefault(nome, []).append(rel(p))
        if ANUNCIOS.search(t):
            reconhece_anuncios = True
    cortar = lambda d: {k: v[:5] for k, v in d.items()}  # noqa: E731

    return {
        "caminho": str(raiz),
        "instrucoes": instrucoes,
        "decisoes": decisoes,
        "estrutura": {"arquivos": len(arquivos), "pastas": dict(sorted(pastas.items(), key=lambda x: -x[1])[:12]),
                      "extensoes": dict(sorted(extensoes.items(), key=lambda x: -x[1])[:8])},
        "arquivos_seo": seo,
        "arquivos_com_jsonld": jsonld,
        "medicao": {"terceiros": cortar(terceiros), "propria": cortar(proprios), "reconhece_cliques_de_anuncios": reconhece_anuncios},
        "privacidade": [rel(p) for p in arquivos if re.search(r"privacidade|privacy", rel(p), re.I)][:5],
        "implantacao": {n: (n in nomes or (raiz / n).exists()) for n in ("vercel.json", ".vercel", "Dockerfile", "docker-compose.yml", "railway.json", "Procfile", "package.json", "requirements.txt")},
        "tem_testes": any("test" in part.lower() for p in arquivos for part in p.relative_to(raiz).parts[:-1]) or any(p.name.startswith("test_") for p in arquivos),
        "pendencias": [rel(p) for p in arquivos if re.search(r"pendencia", p.name, re.I)][:5],
    }
