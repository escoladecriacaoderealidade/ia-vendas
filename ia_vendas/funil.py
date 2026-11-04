"""Mapa simples dos caminhos que saem do site para apps e checkouts (outros endereços).

Hipótese de trabalho (H): links e botões que levam a outro endereço do mesmo domínio ou a um domínio de fora
são os passos seguintes do funil (app, loja, checkout). Quem confirma o que cada destino é: uma pessoa ou a
leitura do repositório do destino.
"""
from __future__ import annotations

from urllib.parse import urlparse


def mapear_funis(site: dict) -> dict:
    paginas = [p for p in site["paginas"] if p.get("status") == 200 and "links" in p]
    destinos: dict[str, dict] = {}
    for p in paginas:
        botoes = {(c["href"], c["texto"]) for c in p.get("ctas", [])}
        secao = "/" + (urlparse(p["url"]).path.strip("/").split("/")[0] if urlparse(p["url"]).path.strip("/") else "")
        for l in p["links"]:
            if l["tipo"] not in ("subdominio", "externo"):
                continue
            u = urlparse(l["href"])
            d = destinos.setdefault(u.netloc.lower(), {"host": u.netloc.lower(), "tipo": l["tipo"], "links": 0, "paginas": set(),
                                                       "secoes_de_origem": {}, "textos": {}, "textos_links": {}, "caminhos": {}})
            d["links"] += 1
            d["paginas"].add(p["url"])
            d["secoes_de_origem"][secao] = d["secoes_de_origem"].get(secao, 0) + 1
            if l["texto"]:
                alvo = d["textos"] if (l["href"], l["texto"]) in botoes else d["textos_links"]
                alvo[l["texto"]] = alvo.get(l["texto"], 0) + 1
            d["caminhos"][u.path or "/"] = d["caminhos"].get(u.path or "/", 0) + 1

    saidas = []
    for d in sorted(destinos.values(), key=lambda x: -x["links"]):
        top = lambda dic, k=5: [{"valor": a, "vezes": b} for a, b in sorted(dic.items(), key=lambda x: -x[1])[:k]]  # noqa: E731
        saidas.append({"host": d["host"], "tipo": d["tipo"], "links": d["links"], "paginas_de_origem": len(d["paginas"]),
                       "secoes_de_origem": top(d["secoes_de_origem"]), "textos_dos_botoes": top(d["textos"] or d["textos_links"]),
                       "destinos_mais_usados": top(d["caminhos"])})
    return {"estatuto": "H", "saidas_para_outros_enderecos": saidas, "paginas_analisadas": len(paginas)}
