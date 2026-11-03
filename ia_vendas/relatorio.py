"""Gera o relatório em Markdown a partir da análise (no formato do diagnóstico inicial do projeto)."""
from __future__ import annotations

from urllib.parse import urlparse

SEV = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}


def _linha(*cols) -> str:
    return "| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in cols) + " |"


def gerar_markdown(analise: dict) -> str:
    site, achados, funil, repo = analise["site"], analise["achados"], analise["funil"], analise.get("repositorio")
    r = site["resumo"]
    host = urlparse(site["base_url"]).netloc
    out: list[str] = []
    w = out.append

    w(f"# Análise de {host}")
    w("")
    w(f"Gerada em {site['coletado_em']} pela IA de Vendas v{analise['versao']}. Estatutos: **I** inferido do que foi lido, **H** hipótese, **D?** candidata a decisão do cliente. Nada aqui é V (verificado em fonte oficial).")
    w("")
    w("## 1. Escopo e limites")
    w(f"- Páginas lidas: **{r['paginas_lidas']}**" + (f" ({r['paginas_com_erro']} com erro ou bloqueio)" if r["paginas_com_erro"] else "")
      + (f". **Leitura truncada** no limite de {site['limites']['max_paginas']} páginas." if site["limites"]["truncado"] else "."))
    w(f"- robots.txt: {'encontrado' if site['robots']['existe'] else 'não encontrado'}; sitemap: {site['sitemap']['urls']} endereços; llms.txt: {'sim' if site['llms_txt'] else 'não'}.")
    w(f"- Repositório do cliente: {'lido (' + str(repo['estrutura']['arquivos']) + ' arquivos)' if repo else 'não informado'}.")
    w("")

    w("## 2. Caminhos que saem do site (funil, hipótese)")
    saidas = funil["saidas_para_outros_enderecos"]
    if saidas:
        w(_linha("Destino", "Tipo", "Links", "Páginas de origem", "Botões mais usados"))
        w(_linha("---", "---", "---", "---", "---"))
        for s in saidas[:12]:
            textos = "; ".join(t["valor"] for t in s["textos_dos_botoes"][:3]) or "(sem texto)"
            w(_linha(s["host"], s["tipo"], s["links"], s["paginas_de_origem"], textos))
    else:
        w("Nenhum link para outro endereço foi encontrado nas páginas lidas.")
    if r["ctas_principais"]:
        w("")
        w("Botões de ação mais repetidos: " + "; ".join(f"\"{c['texto']}\" ({c['vezes']}x)" for c in r["ctas_principais"][:5]) + ".")
    w("")

    w("## 3. Achados")
    if not achados:
        w("Nenhum achado automático. Isso não prova que está tudo certo: veja a seção 6.")
    else:
        w(_linha("Severidade", "Estatuto", "Achado", "Evidência", "Receita", "Atenção"))
        w(_linha("---", "---", "---", "---", "---", "---"))
        for a in achados:
            atencao = "Possível decisão do cliente, confirmar antes de agir" if a["possivel_decisao"] else ""
            w(_linha(SEV[a["severidade"]], a["estatuto"], a["titulo"], a["evidencia"], a["receita"] or "", atencao))
        decididos = [a for a in achados if a["possivel_decisao"]]
        if decididos:
            w("")
            w("**Achados que podem ser decisão deliberada** (regra 5: separar decisão de lacuna):")
            for a in decididos:
                for d in a["possivel_decisao"][:2]:
                    w(f"- {a['titulo']}: `{d['arquivo']}` linha {d['linha']}: \"{d['texto'][:160]}\"")
    w("")

    w("## 4. O que já existe (resumo das páginas)")
    w(f"- Dados estruturados: {', '.join(f'{t} ({n})' for t, n in sorted(r['jsonld_tipos'].items())) or 'nenhum'}.")
    w(f"- Medição de terceiros: {', '.join(r['trackers']) or 'nenhuma encontrada'}; sinais de medição própria em {r['paginas_com_medicao_propria']} página(s).")
    w(f"- Preço visível em {r['paginas_com_preco']} página(s); prova social em {r['paginas_com_prova_social']}; formulários: {r['formularios']} ({r['formularios_com_email']} com e-mail).")
    w("")

    if repo:
        w("## 5. O que o repositório diz")
        w(f"- Arquivos de regras: {', '.join(i['arquivo'] for i in repo['instrucoes']) or 'nenhum'}.")
        w(f"- Medição no código: terceiros: {', '.join(repo['medicao']['terceiros']) or 'nenhuma'}; própria: {', '.join(repo['medicao']['propria']) or 'nenhuma'}; reconhece cliques de anúncios: {'sim' if repo['medicao']['reconhece_cliques_de_anuncios'] else 'não'}.")
        w(f"- Política de privacidade: {', '.join(repo['privacidade']) or 'não encontrada'}. Pendências: {', '.join(repo['pendencias']) or 'nenhum arquivo'}.")
        if repo["decisoes"]:
            w("")
            w(f"Regras e decisões encontradas ({len(repo['decisoes'])}, candidatas a D, confirmar com o dono):")
            for d in repo["decisoes"][:12]:
                w(f"- `{d['arquivo']}:{d['linha']}` {d['texto'][:200]}")
        w("")

    w("## 6. Não verificado (sempre)")
    w("- Tráfego, palavras-chave, conversões e preços dentro de apps: exigem Search Console, Analytics ou o banco do cliente.")
    w("- Conteúdo montado por JavaScript no navegador e scripts carregados de outros endereços: o coletor lê só o HTML recebido.")
    w("- Regras atuais dos mecanismos de venda (Google, Bing, ChatGPT): estão na base de regras do robô diário, não aqui.")
    w("- Público-alvo: sem dados reais, qualquer público é hipótese (H).")
    w("")

    w("## 7. Próximos passos sugeridos")
    receitas = []
    for a in achados:
        if a["receita"] and not a["possivel_decisao"] and a["receita"] not in receitas:
            receitas.append(a["receita"])
    if receitas:
        for rc in receitas:
            w(f"- Aplicar a receita `{rc}`.")
    else:
        w("- Nenhuma receita pronta se aplica automaticamente. Revisar os achados de severidade alta.")
    w("- Antes de mudar qualquer coisa: ponto de recuperação e pull request (CLAUDE.md, regras 1 e 2).")
    w("")
    return "\n".join(out)
