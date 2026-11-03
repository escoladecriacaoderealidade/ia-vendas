"""Linha de comando.

Exemplos:
  python -m ia_vendas analisar --url https://exemplo.com.br --saida resultado
  python -m ia_vendas analisar --dir ../meu-site --url https://exemplo.com.br --repo ../meu-site --saida resultado
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .achados import gerar_achados
from .funil import mapear_funis
from .relatorio import gerar_markdown
from .repositorio import ler_repositorio
from .site import coletar_site, criar_fetch_dir, criar_fetch_http


def analisar(url: str, buscar, repo_caminho: str | None = None, max_paginas: int = 60) -> dict:
    site = coletar_site(url, buscar, max_paginas)
    repo = ler_repositorio(repo_caminho) if repo_caminho else None
    return {"versao": __version__, "site": site, "repositorio": repo,
            "achados": gerar_achados(site, repo), "funil": mapear_funis(site)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ia_vendas", description="IA de Vendas: analisa um site e, se informado, o repositório dele.")
    sub = ap.add_subparsers(dest="comando", required=True)
    a = sub.add_parser("analisar", help="Analisa um site (e opcionalmente o repositório).")
    a.add_argument("--url", required=True, help="Endereço do site, com https://")
    a.add_argument("--dir", action="append", help="Pasta com os arquivos do site (modo sem rede). Pode repetir: vale a primeira pasta que tiver o arquivo. A --url continua sendo o endereço real.")
    a.add_argument("--repo", help="Pasta do repositório do cliente (clone local).")
    a.add_argument("--max-paginas", type=int, default=60)
    a.add_argument("--intervalo", type=float, default=1.0, help="Segundos entre pedidos (padrão 1).")
    a.add_argument("--saida", default="resultado", help="Pasta onde gravar analise.json e relatorio.md")
    args = ap.parse_args(argv)

    buscar = criar_fetch_dir(args.dir) if args.dir else criar_fetch_http(intervalo=args.intervalo)
    try:
        analise = analisar(args.url, buscar, args.repo, args.max_paginas)
    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 2

    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "analise.json").write_text(json.dumps(analise, ensure_ascii=False, indent=2), encoding="utf-8")
    (saida / "relatorio.md").write_text(gerar_markdown(analise), encoding="utf-8")

    r = analise["site"]["resumo"]
    print(f"Páginas lidas: {r['paginas_lidas']} | achados: {len(analise['achados'])} "
          f"(alta: {sum(1 for x in analise['achados'] if x['severidade'] == 'alta')})")
    print(f"Gravado em: {saida / 'analise.json'} e {saida / 'relatorio.md'}")
    return 0 if r["paginas_lidas"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
