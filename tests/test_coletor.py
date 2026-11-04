from ia_vendas.coletor import analisar_html, dominio_base, tipo_link
from tests.conftest import HOME, SEM_NADA, LIVROS

URL = "https://exemplo.com.br/"


def test_dominio_base():
    assert dominio_base("enquanto.escoladecriacaoderealidade.com.br") == "escoladecriacaoderealidade.com.br"
    assert dominio_base("www.enquantoestuda.com.br") == "enquantoestuda.com.br"
    assert dominio_base("app.exemplo.org") == "exemplo.org"
    assert dominio_base("EXEMPLO.COM:8080") == "exemplo.com"


def test_tipo_link():
    assert tipo_link("https://www.exemplo.com.br/x", "exemplo.com.br") == "interno"
    assert tipo_link("https://app.exemplo.com.br/", "exemplo.com.br") == "subdominio"
    assert tipo_link("https://outro.com/", "exemplo.com.br") == "externo"
    assert tipo_link("mailto:a@b.com", "exemplo.com.br") == "contato"


def test_basico_de_busca_e_compartilhamento():
    a = analisar_html(HOME, URL)
    assert a["titulo"] == "Loja Exemplo" and a["descricao"] == "Livros e cursos"
    assert a["canonical"] == "https://exemplo.com.br/" and a["lang"] == "pt-BR" and a["robots_meta"] == "index,follow"
    assert a["og"]["og:image"].endswith("capa.jpg") and a["twitter"]["twitter:card"] == "summary"
    assert a["n_h1"] == 1 and a["titulos"]["h2"] == ["Livros"]


def test_jsonld_com_graph_lista_de_tipos_e_bloco_invalido():
    a = analisar_html(HOME, URL)
    assert a["jsonld"]["blocos"] == 2 and a["jsonld"]["invalidos"] == 1
    assert a["jsonld"]["tipos"] == ["Book", "Organization", "Product"]


def test_links_botoes_e_formularios():
    a = analisar_html(HOME, URL)
    por_texto = {l["texto"]: l for l in a["links"]}
    assert por_texto["Ver livros"]["tipo"] == "interno" and por_texto["Ver livros"]["href"] == "https://exemplo.com.br/livros/"
    assert por_texto["Abrir o app"]["tipo"] == "subdominio"
    assert "#" not in por_texto["Abrir o app"]["href"]           # fragmento removido
    assert por_texto["Comprar fora"]["tipo"] == "externo" and por_texto["Contato"]["tipo"] == "contato"
    assert "pular" not in por_texto and "nada" not in por_texto    # âncora interna e javascript: ficam de fora
    assert {c["texto"] for c in a["ctas"]} == {"Ver livros", "Abrir o app"}   # classes btn e read-button
    assert a["formularios"] == [{"campos": ["text", "email", "textarea"], "tem_email": True}]


def test_imagens_alt_vazio_conta_como_decorativo():
    a = analisar_html(HOME, URL)
    assert a["imagens"] == {"total": 3, "sem_alt": 1}


def test_medicao_preco_prova_social_e_privacidade():
    a = analisar_html(HOME, URL)
    assert a["trackers"] == ["Google Analytics / Tag Manager", "Meta Pixel"]
    assert a["tem_preco"] is True            # "R$ 29,90" no texto visível; o R$ de <script> e <style> não conta
    assert a["tem_prova_social"] is True and a["tem_link_privacidade"] is True
    assert a["medicao_propria_dica"] is False


def test_preco_so_em_script_ou_estilo_nao_conta():
    html = "<html><head><style>a::after{content:'R$ 5'}</style></head><body><script>var x='R$ 9'</script><p>oi</p></body></html>"
    assert analisar_html(html, URL)["tem_preco"] is False


def test_pagina_vazia_e_h1_duplicado():
    v = analisar_html(SEM_NADA, URL)
    assert v["titulo"] is None and v["descricao"] is None and v["canonical"] is None and v["n_h1"] == 0
    assert v["jsonld"] == {"blocos": 0, "tipos": [], "invalidos": 0}
    assert analisar_html(LIVROS, URL)["n_h1"] == 2


def test_medicao_propria_por_sendbeacon_e_arquivo_medir():
    html = '<script>navigator.sendBeacon("/api/visita", "{}")</script>'
    assert analisar_html(html, URL)["medicao_propria_dica"] is True
    assert analisar_html('<script src="/medir.js" defer></script>', URL)["medicao_propria_dica"] is True


def test_html_quebrado_nao_derruba():
    a = analisar_html("<html><body><a href='/x'>sem fechar<div><p>texto", URL)
    assert a["links"][0]["href"] == "https://exemplo.com.br/x"
