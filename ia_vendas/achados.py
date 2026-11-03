"""Transforma o resumo do site (e, se houver, do repositório) em achados.

Regra 5 do CLAUDE.md: separar decisão deliberada de lacuna. Cada achado leva "chaves"; se uma regra/decisão do
cliente (linhas do CLAUDE.md etc.) contém uma dessas palavras, o achado sai com "possivel_decisao" e NÃO deve ser
tratado como falha sem confirmar com o dono. Todo achado é estatuto I (inferido) ou H (hipótese).
"""
from __future__ import annotations

ORDEM = {"alta": 0, "media": 1, "baixa": 2}
RECEITAS = {
    "og": "receitas/compartilhamento-og-twitter.md",
    "visitas": "receitas/visita-de-pagina-e-cliques.md",
    "anuncios": "receitas/canal-de-anuncios-nas-estatisticas.md",
    "cadastro": "receitas/canal-do-cadastro.md",
}


def _decisoes(repo: dict | None, chaves: tuple[str, ...]) -> list[dict]:
    if not repo or not chaves:
        return []
    achadas = []
    for d in repo.get("decisoes", []):
        texto = d["texto"].lower()
        if any(c.lower() in texto for c in chaves):
            achadas.append({"arquivo": d["arquivo"], "linha": d["linha"], "texto": d["texto"]})
    return achadas[:3]


def gerar_achados(site: dict, repo: dict | None = None) -> list[dict]:
    r = site["resumo"]
    n = r["paginas_lidas"]
    achados: list[dict] = []

    def add(id_, titulo, severidade, evidencia, receita=None, chaves=(), estatuto="I"):
        achados.append({"id": id_, "titulo": titulo, "estatuto": estatuto, "severidade": severidade,
                        "evidencia": evidencia, "receita": RECEITAS.get(receita), "possivel_decisao": _decisoes(repo, tuple(chaves))})

    if n == 0:
        add("sem_paginas", "Nenhuma página pôde ser lida", "alta",
            f"{r['paginas_com_erro']} endereço(s) falharam. Pode ser bloqueio do robots.txt, site fora do ar, endereço errado, ou um aplicativo que monta a página por JavaScript (o coletor lê só HTML).")
        # Sem páginas não dá para afirmar nada sobre o site, mas o que vem só do código continua valendo.
        if repo and repo["medicao"]["propria"] and not repo["medicao"]["reconhece_cliques_de_anuncios"]:
            add("anuncios_nao_reconhecidos", "A medição não reconhece cliques de anúncios (gclid, msclkid, fbclid)", "media",
                "nenhuma referência a esses parâmetros no código", "anuncios", chaves=("gclid", "msclkid", "fbclid", "utm_", "parâmetros de anúncio"))
        return achados

    de = lambda x: f"em {x} de {n} páginas"  # noqa: E731

    # Básico de busca
    if r["sem_titulo"]:
        add("sem_titulo", "Páginas sem título", "alta", de(r["sem_titulo"]))
    if r["sem_descricao"]:
        add("sem_descricao", "Páginas sem descrição para os buscadores", "alta", de(r["sem_descricao"]))
    if r["sem_canonical"]:
        add("sem_canonical", "Páginas sem endereço canônico", "media", de(r["sem_canonical"]))
    if r["paginas_sem_h1"]:
        add("sem_h1", "Páginas sem título principal (h1)", "media", de(r["paginas_sem_h1"]))
    if r["paginas_h1_multiplos"]:
        add("h1_multiplos", "Páginas com mais de um título principal (h1)", "baixa", de(r["paginas_h1_multiplos"]))
    if r["imagens_sem_alt"]:
        add("imagens_sem_alt", "Imagens sem texto alternativo", "media", f"{r['imagens_sem_alt']} de {r['imagens_total']} imagens")

    # Compartilhamento e dados estruturados
    if r["sem_og_image"]:
        add("sem_og_image", "Link compartilhado sem imagem (og:image)", "media", de(r["sem_og_image"]), "og")
    if r["sem_twitter_card"]:
        add("sem_twitter_card", "Sem cartão do X/Twitter", "baixa", de(r["sem_twitter_card"]), "og")
    if r["sem_jsonld"]:
        add("sem_jsonld", "Páginas sem dados estruturados (JSON-LD)", "media", de(r["sem_jsonld"]))
    if r["jsonld_invalidos"]:
        add("jsonld_invalido", "Dados estruturados com erro de formato", "alta", f"{r['jsonld_invalidos']} bloco(s) inválido(s)")

    # Rastreadores e buscadores de IA
    robots = site["robots"]
    if not robots["existe"]:
        add("sem_robots", "Sem robots.txt", "media", "arquivo não encontrado")
    if robots["bloqueia_tudo"]:
        add("robots_bloqueia_tudo", "O robots.txt bloqueia todos os robôs", "alta", "User-agent: * com Disallow: /")
    if robots["ia_bloqueada"]:
        add("robots_bloqueia_ia", "O robots.txt bloqueia robôs de busca ou de IA", "alta", ", ".join(robots["ia_bloqueada"]),
            chaves=("robô", "robots", "gptbot", "claudebot", "bloquear robô"))
    if not site["sitemap"]["arquivos"]:
        add("sem_sitemap", "Sem sitemap.xml", "media", "arquivo não encontrado")
    if not site["llms_txt"]:
        add("sem_llms", "Sem llms.txt (guia para IAs)", "baixa", "arquivo não encontrado")

    # Medição
    terceiros, proprias = r["trackers"], r["paginas_com_medicao_propria"]
    repo_proprio = bool(repo and repo["medicao"]["propria"])
    tem_medicao = bool(terceiros) or proprias > 0
    if not tem_medicao:
        if repo_proprio:
            add("medicao_so_no_app", "A medição própria existe no código, mas não aparece nas páginas lidas", "media",
                "arquivos: " + ", ".join(sorted({f for v in repo["medicao"]["propria"].values() for f in v})[:4]),
                "visitas", chaves=("medição", "medicao", "analytics", "estatíst", "cookie", "rastre"))
        else:
            add("sem_medicao", "Nenhuma medição de visitas encontrada", "alta",
                "sem Google Analytics, Meta Pixel, Clarity, Hotjar e sem envio de eventos próprio nas páginas lidas",
                "visitas", chaves=("medição", "medicao", "analytics", "estatíst", "cookie", "rastre"))
    if repo_proprio and not repo["medicao"]["reconhece_cliques_de_anuncios"]:
        add("anuncios_nao_reconhecidos", "A medição não reconhece cliques de anúncios (gclid, msclkid, fbclid)", "media",
            "nenhuma referência a esses parâmetros no código", "anuncios", chaves=("gclid", "msclkid", "fbclid", "utm_", "parâmetros de anúncio"))
    if tem_medicao and r["paginas_com_link_privacidade"] == 0:
        add("medicao_sem_privacidade", "Há medição, mas nenhuma página tem link para a política de privacidade", "alta",
            "nenhum link com 'privacidade' nas páginas lidas", chaves=("privacidade", "lgpd"))

    # Conversão
    if r["formularios_com_email"] == 0:
        add("sem_captura_email", "Sem captura de e-mail (formulário com campo de e-mail)", "media",
            "nenhum formulário com e-mail nas páginas lidas", chaves=("e-mail", "email", "lead", "captura", "formulário"))
    if r["paginas_com_preco"] == 0:
        vende_fora = bool(r["destinos_fora_do_host"])
        add("sem_preco_visivel", "Nenhum preço (R$) aparece nas páginas lidas", "baixa",
            "o preço pode estar no destino dos botões" if vende_fora else "nenhuma página cita valor",
            chaves=("preço", "preco", "valor", "r$"), estatuto="H")
    if r["paginas_com_prova_social"] == 0:
        add("sem_prova_social", "Sem prova social (depoimentos, avaliações)", "media",
            "nenhuma palavra de depoimento ou avaliação nas páginas lidas", chaves=("depoimento", "avalia", "prova social"))

    achados.sort(key=lambda a: (ORDEM[a["severidade"]], a["id"]))
    return achados
