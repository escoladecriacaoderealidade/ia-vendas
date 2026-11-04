import json

from ia_vendas.cli import main
from ia_vendas.funil import mapear_funis
from ia_vendas.relatorio import gerar_markdown
from ia_vendas.site import coletar_site, criar_fetch_dir

BASE = "https://exemplo.com.br/"


def test_funil_aponta_os_destinos_fora_do_host(site_dir):
    f = mapear_funis(coletar_site(BASE, criar_fetch_dir(site_dir)))
    hosts = {s["host"]: s for s in f["saidas_para_outros_enderecos"]}
    assert set(hosts) == {"app.exemplo.com.br", "loja.parceiro.com"}
    app = hosts["app.exemplo.com.br"]
    assert app["tipo"] == "subdominio" and app["links"] == 1
    assert app["textos_dos_botoes"] == [{"valor": "Abrir o app", "vezes": 1}]       # só texto de botão
    assert hosts["loja.parceiro.com"]["textos_dos_botoes"] == [{"valor": "Comprar fora", "vezes": 1}]   # sem botão: cai nos links
    assert f["estatuto"] == "H"


def test_linha_de_comando_ponta_a_ponta(site_dir, tmp_path, capsys):
    (tmp_path / "repo").mkdir()
    (tmp_path / "repo" / "CLAUDE.md").write_text("- **Nunca** prometer resultado.\n", encoding="utf-8")
    saida = tmp_path / "saida"
    code = main(["analisar", "--url", BASE, "--dir", str(site_dir), "--repo", str(tmp_path / "repo"), "--saida", str(saida)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Páginas lidas: 3" in out
    analise = json.loads((saida / "analise.json").read_text(encoding="utf-8"))
    assert set(analise) == {"versao", "site", "repositorio", "achados", "funil"}
    md = (saida / "relatorio.md").read_text(encoding="utf-8")
    for secao in ("# Análise de exemplo.com.br", "## 1. Escopo e limites", "## 3. Achados", "## 6. Não verificado (sempre)", "## 7. Próximos passos"):
        assert secao in md
    assert "Nada aqui é V" in md and md == gerar_markdown(analise)


def test_codigos_de_saida(tmp_path, site_dir, capsys):
    assert main(["analisar", "--url", BASE, "--dir", str(tmp_path / "vazia"), "--saida", str(tmp_path / "s1")]) == 1      # nada lido
    assert main(["analisar", "--url", BASE, "--dir", str(site_dir), "--repo", str(tmp_path / "nao-existe"), "--saida", str(tmp_path / "s2")]) == 2
    assert "Pasta não encontrada" in capsys.readouterr().err


def test_cli_aceita_varias_pastas(site_dir, tmp_path):
    camada = tmp_path / "camada"
    camada.mkdir()
    (camada / "index.html").write_text("<html><head><title>Camada</title></head><body>oi</body></html>")
    assert main(["analisar", "--url", BASE, "--dir", str(camada), "--dir", str(site_dir), "--saida", str(tmp_path / "s")]) == 0
    analise = json.loads((tmp_path / "s" / "analise.json").read_text(encoding="utf-8"))
    assert analise["site"]["paginas"][0]["titulo"] == "Camada"
