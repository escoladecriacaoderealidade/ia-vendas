import http.server
import threading
import urllib.request

import pytest

from ia_vendas.site import BLOQUEADO_POR_ROBOTS, coletar_site, criar_fetch_dir, criar_fetch_http, _analisar_robots

BASE = "https://exemplo.com.br/"


def test_fetch_dir_serve_index_arquivos_e_404(site_dir):
    b = criar_fetch_dir(site_dir)
    assert b(BASE)[0] == 200 and "Loja Exemplo" in b(BASE)[2]
    assert b(BASE + "livros/")[0] == 200 and b(BASE + "livros")[0] == 200      # com e sem barra final
    assert b(BASE + "robots.txt")[1] == "text/plain"
    assert b(BASE + "nao-existe/")[0] == 404


def test_fetch_dir_nao_sai_da_pasta(site_dir, tmp_path_factory):
    segredo = tmp_path_factory.mktemp("fora") / "segredo.txt"
    segredo.write_text("senha", encoding="utf-8")
    b = criar_fetch_dir(site_dir)
    assert b(BASE + "../" + segredo.parent.name + "/segredo.txt")[0] == 404
    assert b(BASE + "..%2f..%2fetc/passwd")[0] == 404


def test_robots_agentes_bloqueios_e_sitemaps():
    r = _analisar_robots((200, "text/plain", "User-agent: *\nDisallow: /privado\nUser-agent: GPTBot\nUser-agent: ClaudeBot\nDisallow: /\nSitemap: https://x/s.xml # c"))
    assert r["existe"] and r["bloqueia_tudo"] is False
    assert r["ia_bloqueada"] == ["GPTBot", "ClaudeBot"]          # dois agentes no mesmo grupo
    assert r["sitemaps"] == ["https://x/s.xml"]
    assert _analisar_robots((200, "", "User-agent: *\nDisallow: /"))["bloqueia_tudo"] is True
    assert _analisar_robots((404, "", ""))["existe"] is False


def test_coletar_site_com_sitemap(site_dir):
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    urls = [p["url"] for p in s["paginas"]]
    assert urls == [BASE, BASE + "livros/", BASE + "vazio/"]       # home uma vez só; domínio de fora ignorado
    assert s["sitemap"]["urls"] == 3 and s["llms_txt"] is False
    assert s["robots"]["ia_bloqueada"] == ["GPTBot"]
    r = s["resumo"]
    assert r["paginas_lidas"] == 3 and r["paginas_com_erro"] == 0
    assert r["sem_titulo"] == 1 and r["sem_descricao"] == 2 and r["sem_og_image"] == 2 and r["sem_jsonld"] == 2
    assert r["paginas_h1_multiplos"] == 1 and r["paginas_sem_h1"] == 1
    assert r["jsonld_invalidos"] == 1 and r["jsonld_tipos"]["Book"] == 1
    assert set(r["trackers"]) == {"Google Analytics / Tag Manager", "Meta Pixel"}
    assert r["formularios"] == 1 and r["formularios_com_email"] == 1
    assert r["paginas_com_preco"] == 1 and r["paginas_com_prova_social"] == 1
    assert r["destinos_fora_do_host"]["app.exemplo.com.br"] == {"tipo": "subdominio", "links": 1, "paginas": 1}
    assert r["destinos_fora_do_host"]["loja.parceiro.com"]["tipo"] == "externo"


def test_limite_de_paginas_marca_truncado(site_dir):
    s = coletar_site(BASE, criar_fetch_dir(site_dir), max_paginas=2)
    assert s["limites"] == {"max_paginas": 2, "paginas_lidas": 2, "truncado": True}


def test_descobre_paginas_pelos_links_quando_nao_ha_sitemap(site_dir):
    (site_dir / "sitemap.xml").unlink()
    (site_dir / "robots.txt").unlink()
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    # /vazio/ não recebe link de ninguém: não é achada. /privacidade/ é linkada pela home mas não existe: link quebrado detectado.
    assert {p["url"] for p in s["paginas"]} == {BASE, BASE + "livros/", BASE + "privacidade/"}
    assert s["paginas"][-1] == {"url": BASE + "privacidade/", "status": 404}
    assert s["resumo"]["paginas_lidas"] == 2 and s["resumo"]["paginas_com_erro"] == 1
    assert s["robots"]["existe"] is False and s["sitemap"]["arquivos"] == []


def test_pagina_com_erro_entra_na_contagem(site_dir):
    (site_dir / "sitemap.xml").write_text("<urlset><url><loc>https://exemplo.com.br/</loc></url><url><loc>https://exemplo.com.br/sumiu/</loc></url></urlset>")
    s = coletar_site(BASE, criar_fetch_dir(site_dir))
    assert s["resumo"]["paginas_lidas"] == 1 and s["resumo"]["paginas_com_erro"] == 1
    assert s["paginas"][1] == {"url": BASE + "sumiu/", "status": 404}


# ----------------------------------------------------------- buscador de internet, contra um servidor local
class _Servidor(http.server.BaseHTTPRequestHandler):
    agentes: list[str] = []
    pedidos: list[str] = []

    def do_GET(self):
        _Servidor.agentes.append(self.headers.get("User-Agent", ""))
        _Servidor.pedidos.append(self.path)
        rotas = {
            "/robots.txt": ("text/plain", "User-agent: *\nDisallow: /privado/\n"),
            "/": ("text/html; charset=utf-8", "<html><head><title>Oi</title></head><body>ola</body></html>"),
            "/privado/": ("text/html", "<html>segredo</html>"),
            "/imagem.png": ("image/png", "PNG"),
        }
        if self.path in rotas:
            tipo, corpo = rotas[self.path]
            self.send_response(200); self.send_header("Content-Type", tipo); self.end_headers(); self.wfile.write(corpo.encode())
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *a):
        pass


@pytest.fixture
def servidor(monkeypatch):
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    _Servidor.agentes, _Servidor.pedidos = [], []
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Servidor)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def test_http_respeita_robots_identifica_o_robo_e_trata_erros(servidor):
    b = criar_fetch_http(intervalo=0, timeout=3)
    assert b(servidor + "/")[0] == 200 and "Oi" in b(servidor + "/")[2]
    assert b(servidor + "/privado/") == (BLOQUEADO_POR_ROBOTS, "", "")
    assert "/privado/" not in _Servidor.pedidos                      # nem chegou a pedir
    assert b(servidor + "/nada")[0] == 404
    assert b(servidor + "/imagem.png") [2] == ""                     # não baixa o que não é texto
    assert all(a.startswith("IAVendasBot/") for a in _Servidor.agentes)
    falha = criar_fetch_http(intervalo=0, timeout=1)("http://127.0.0.1:1/")
    assert falha[0] == 0 and falha[2] != ""                          # sem servidor: falha de rede, com o motivo


def test_http_pode_ignorar_robots_so_se_pedirem(servidor):
    b = criar_fetch_http(intervalo=0, respeitar_robots=False)
    assert b(servidor + "/privado/")[0] == 200


def test_coletar_site_pela_internet_local(servidor):
    s = coletar_site(servidor + "/", criar_fetch_http(intervalo=0), max_paginas=5)
    assert s["resumo"]["paginas_lidas"] == 1 and s["robots"]["existe"] is True


def test_varias_pastas_sobrepostas(site_dir, tmp_path):
    camada = tmp_path / "camada"
    camada.mkdir()
    (camada / "index.html").write_text("<html><head><title>Home da camada</title></head><body>ola</body></html>")
    b = criar_fetch_dir([camada, site_dir])
    assert "Home da camada" in b(BASE)[2]                 # a primeira pasta vence
    assert b(BASE + "livros/")[0] == 200                   # o resto vem da segunda
    assert b(BASE + "nada/")[0] == 404


def test_motivo_da_falha_de_rede_chega_ao_achado():
    from ia_vendas.achados import gerar_achados
    quebrado = lambda url: (0, "", "SSLCertVerificationError: certificate verify failed")   # noqa: E731
    s = coletar_site(BASE, quebrado)
    assert s["paginas"][0] == {"url": BASE, "status": 0, "erro": "SSLCertVerificationError: certificate verify failed"}
    achado = gerar_achados(s)[0]
    assert achado["id"] == "sem_paginas" and "SSLCertVerificationError" in achado["evidencia"]
