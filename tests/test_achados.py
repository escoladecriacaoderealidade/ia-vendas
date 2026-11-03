from ia_vendas.achados import gerar_achados
from ia_vendas.site import coletar_site, criar_fetch_dir

BASE = "https://exemplo.com.br/"


def _ids(achados):
    return {a["id"] for a in achados}


def _por_id(achados, id_):
    return next(a for a in achados if a["id"] == id_)


def _repo(decisoes=(), propria=None, terceiros=None, anuncios=False, privacidade=()):
    return {"decisoes": [{"arquivo": "CLAUDE.md", "linha": i + 1, "texto": t, "estatuto": "D?"} for i, t in enumerate(decisoes)],
            "medicao": {"terceiros": terceiros or {}, "propria": propria or {}, "reconhece_cliques_de_anuncios": anuncios},
            "privacidade": list(privacidade)}


def test_achados_do_site_de_exemplo(site_dir):
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    a = gerar_achados(s)
    ids = _ids(a)
    assert {"sem_titulo", "sem_descricao", "sem_og_image", "sem_jsonld", "jsonld_invalido", "h1_multiplos", "sem_h1",
            "imagens_sem_alt", "robots_bloqueia_ia", "sem_llms"} <= ids
    assert "sem_medicao" not in ids and "sem_captura_email" not in ids and "sem_twitter_card" in ids
    assert _por_id(a, "sem_og_image")["receita"] == "receitas/compartilhamento-og-twitter.md"
    assert _por_id(a, "robots_bloqueia_ia")["evidencia"] == "GPTBot"
    ordem = [x["severidade"] for x in a]
    assert ordem == sorted(ordem, key=["alta", "media", "baixa"].index)      # alta primeiro


def test_decisao_deliberada_nao_vira_falha(site_dir):
    """Lição do caso da Escola: 'sem preço no site' era regra do dono."""
    (site_dir / "index.html").write_text("<!doctype html><html><head><title>x</title></head><body><a href='https://app.exemplo.com.br/'>App</a></body></html>")
    (site_dir / "livros" / "index.html").write_text("<html><head><title>y</title></head><body>oi</body></html>")
    (site_dir / "vazio" / "index.html").write_text("<html><head><title>z</title></head><body>oi</body></html>")
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    sem_regra = _por_id(gerar_achados(s), "sem_preco_visivel")
    assert sem_regra["possivel_decisao"] == [] and sem_regra["estatuto"] == "H"
    com_regra = _por_id(gerar_achados(s, _repo(["Fonte da verdade: livros. **Não copiar preços para o site**."])), "sem_preco_visivel")
    assert com_regra["possivel_decisao"][0]["texto"].startswith("Fonte da verdade")
    assert com_regra["possivel_decisao"][0]["linha"] == 1


def test_sem_medicao_e_alta_e_medicao_so_no_codigo_e_media(site_dir):
    (site_dir / "index.html").write_text("<html><head><title>x</title></head><body>oi</body></html>")
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    assert _por_id(gerar_achados(s), "sem_medicao")["severidade"] == "alta"
    com_codigo = gerar_achados(s, _repo(propria={"rota de eventos": ["api/evento.js"]}))
    assert "sem_medicao" not in _ids(com_codigo)
    assert _por_id(com_codigo, "medicao_so_no_app")["severidade"] == "media"
    assert _por_id(com_codigo, "anuncios_nao_reconhecidos")["receita"] == "receitas/canal-de-anuncios-nas-estatisticas.md"
    assert "anuncios_nao_reconhecidos" not in _ids(gerar_achados(s, _repo(propria={"x": ["a.js"]}, anuncios=True)))


def test_medicao_sem_link_de_privacidade_e_alta(site_dir):
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    assert "medicao_sem_privacidade" not in _ids(gerar_achados(s))            # a home de exemplo linka /privacidade/
    s["resumo"]["paginas_com_link_privacidade"] = 0
    assert _por_id(gerar_achados(s), "medicao_sem_privacidade")["severidade"] == "alta"


def test_site_que_nao_pode_ser_lido(tmp_path):
    s = coletar_site(BASE, criar_fetch_dir(tmp_path))
    a = gerar_achados(s)
    assert [x["id"] for x in a] == ["sem_paginas"] and a[0]["severidade"] == "alta"
    # Sem páginas, o que vem só do código do repositório continua valendo (e nada sobre o site é afirmado).
    com_repo = gerar_achados(s, _repo(propria={"rota de eventos": ["api/evento.js"]}))
    assert [x["id"] for x in com_repo] == ["sem_paginas", "anuncios_nao_reconhecidos"]


def test_palavra_ampla_nao_vira_falsa_decisao(site_dir):
    """'sem anúncios intrusivos' (regra de produto) não é decisão de ignorar cliques de anúncios pagos."""
    (site_dir / "index.html").write_text("<html><head><title>x</title></head><body>oi</body></html>")
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    repo = _repo(["Modelo gratuito, sem anúncios intrusivos."], propria={"rota de eventos": ["a.js"]})
    assert _por_id(gerar_achados(s, repo), "anuncios_nao_reconhecidos")["possivel_decisao"] == []
    repo2 = _repo(["Não medir gclid: decisão do dono."], propria={"rota de eventos": ["a.js"]})
    assert len(_por_id(gerar_achados(s, repo2), "anuncios_nao_reconhecidos")["possivel_decisao"]) == 1
