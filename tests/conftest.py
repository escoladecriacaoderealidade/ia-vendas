from pathlib import Path

import pytest

HOME = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Loja Exemplo</title>
<meta name="description" content="Livros e cursos">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://exemplo.com.br/">
<meta property="og:title" content="Loja Exemplo"><meta property="og:image" content="https://exemplo.com.br/capa.jpg">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Organization","name":"Loja"},{"@type":["Book","Product"],"name":"Livro"}]}</script>
<script type="application/ld+json">{ isto nao e json }</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TESTE"></script>
<script>window.dataLayer=[];function gtag(){} gtag('js', new Date()); !function(){fbq('init','1')}();</script>
<style>.preco::after{content:"R$ 99"}</style>
</head><body>
<h1>Bem-vindo</h1><h2>Livros</h2>
<a class="btn" href="/livros/">Ver livros</a>
<a href="https://app.exemplo.com.br/entrar?x=1#topo" class="read-button">Abrir o app</a>
<a href="https://loja.parceiro.com/produto">Comprar fora</a>
<a href="mailto:oi@exemplo.com.br">Contato</a>
<a href="#conteudo">pular</a><a href="javascript:void(0)">nada</a>
<a href="/privacidade/">Política de privacidade</a>
<img src="a.jpg" alt="Capa"><img src="b.jpg"><img src="c.jpg" alt="">
<form><input type="text" name="nome"><input type="email" name="email"><textarea></textarea></form>
<p>Depoimentos de leitores. Livro por R$ 29,90.</p>
<script>var preco = "R$ 1000";</script>
</body></html>"""

LIVROS = """<!doctype html><html lang="pt-BR"><head><title>Livros</title></head>
<body><h1>Livros</h1><h1>Outro h1</h1><a href="/">Início</a></body></html>"""

SEM_NADA = "<!doctype html><html><body><p>oi</p></body></html>"

ROBOTS = "User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nDisallow: /\n\nSitemap: https://exemplo.com.br/sitemap.xml\n"
SITEMAP = """<?xml version="1.0"?><urlset>
<url><loc>https://exemplo.com.br/</loc></url>
<url><loc>https://exemplo.com.br/livros/</loc></url>
<url><loc>https://exemplo.com.br/vazio/</loc></url>
<url><loc>https://outro-dominio.com/fora/</loc></url>
</urlset>"""


@pytest.fixture
def site_dir(tmp_path: Path) -> Path:
    (tmp_path / "index.html").write_text(HOME, encoding="utf-8")
    (tmp_path / "livros").mkdir()
    (tmp_path / "livros" / "index.html").write_text(LIVROS, encoding="utf-8")
    (tmp_path / "vazio").mkdir()
    (tmp_path / "vazio" / "index.html").write_text(SEM_NADA, encoding="utf-8")
    (tmp_path / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (tmp_path / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    return tmp_path
