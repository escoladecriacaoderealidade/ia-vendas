import pytest

from ia_vendas.repositorio import ler_repositorio

CLAUDE = """# Projeto
## Regras
- **Nunca** prometer resultado garantido.
- Texto qualquer sem regra.
Fonte da verdade: livros. **Não copiar preços para o site**: eles mudam.
1. Não mexer em DNS sem avisar.
## Outro
Tudo certo por aqui.
"""


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "CLAUDE.md").write_text(CLAUDE, encoding="utf-8")
    (tmp_path / "README.md").write_text("- Nunca isto aparece como decisão\n", encoding="utf-8")
    (tmp_path / "robots.txt").write_text("User-agent: *\n", encoding="utf-8")
    (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
    (tmp_path / "privacidade").mkdir()
    (tmp_path / "privacidade" / "index.html").write_text("<p>politica</p>", encoding="utf-8")
    (tmp_path / "app.js").write_text("navigator.sendBeacon('/api/evento', x); const c = q.get('gclid');", encoding="utf-8")
    (tmp_path / "pagina.html").write_text('<script type="application/ld+json">{}</script><script>fbq("init")</script>', encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_x.py").write_text("def test_a(): pass", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "pendencias.md").write_text("- [ ] algo", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "lixo.js").write_text("gtag('x')", encoding="utf-8")
    (tmp_path / "vercel.json").write_text("{}", encoding="utf-8")
    return tmp_path


def test_decisoes_em_lista_e_em_paragrafo_e_readme_fica_de_fora(repo):
    r = ler_repositorio(repo)
    textos = [d["texto"] for d in r["decisoes"]]
    assert any("Nunca" in t and "resultado" in t for t in textos)
    assert any("Não copiar preços" in t for t in textos)            # parágrafo, não lista
    assert any("DNS" in t for t in textos)                          # lista numerada
    assert not any("isto aparece" in t for t in textos)             # README não entra
    assert not any(t.startswith("#") for t in textos)
    assert all(d["estatuto"] == "D?" for d in r["decisoes"])
    assert [i["arquivo"] for i in r["instrucoes"]] == ["CLAUDE.md", "README.md"]


def test_seo_medicao_privacidade_implantacao(repo):
    r = ler_repositorio(repo)
    assert r["arquivos_seo"]["robots.txt"] == ["robots.txt"] and r["arquivos_seo"]["llms.txt"] == []
    assert r["arquivos_com_jsonld"] == 1
    assert list(r["medicao"]["propria"]) == ["envio de eventos (sendBeacon)", "rota de eventos"]
    assert "Meta Pixel" in r["medicao"]["terceiros"]
    assert "Google Analytics / Tag Manager" not in r["medicao"]["terceiros"]      # node_modules é ignorado
    assert r["medicao"]["reconhece_cliques_de_anuncios"] is True
    assert r["privacidade"] == ["privacidade/index.html"]
    assert r["implantacao"]["vercel.json"] is True and r["implantacao"]["Dockerfile"] is False
    assert r["tem_testes"] is True and r["pendencias"] == ["docs/pendencias.md"]


def test_pasta_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        ler_repositorio(tmp_path / "nao-existe")
