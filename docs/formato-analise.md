# Formato do `analise.json`

Gerado por `python -m ia_vendas analisar`. Todas as chaves em português. Estatutos: **I** inferido do que foi lido, **H** hipótese, **D?** candidata a decisão do cliente. Nada é V (verificado em fonte oficial): isso é papel do robô diário.

| Chave | Conteúdo |
|---|---|
| `versao` | Versão do programa |
| `site.base_url`, `site.coletado_em` | Endereço analisado e data/hora (UTC) |
| `site.robots` | `existe`, `agentes`, `ia_bloqueada` (robôs de busca/IA com `Disallow: /`), `bloqueia_tudo`, `sitemaps` |
| `site.llms_txt` | Se existe `/llms.txt` |
| `site.sitemap` | Arquivos lidos e quantidade de endereços do mesmo domínio |
| `site.paginas[]` | Por página: `url`, `status` e, se lida, título, descrição, canonical, `og`, `twitter`, `jsonld` (tipos, inválidos), títulos, `links[]` (`tipo`: interno, subdominio, externo, contato), `ctas[]`, `formularios[]`, `imagens`, `trackers`, `medicao_propria_dica`, `tem_preco`, `tem_prova_social`, `tem_link_privacidade` |
| `site.resumo` | Contagens do site inteiro (`sem_og_image`, `paginas_com_preco`, `trackers`, `destinos_fora_do_host`...) |
| `site.limites` | `max_paginas`, `paginas_lidas`, `truncado` (leitura cortada no limite) |
| `repositorio` | Ou `null`. `instrucoes`, `decisoes[]` (D?), `estrutura`, `arquivos_seo`, `arquivos_com_jsonld`, `medicao` (terceiros, própria, reconhece anúncios), `privacidade`, `implantacao`, `tem_testes`, `pendencias` |
| `achados[]` | `id`, `titulo`, `estatuto`, `severidade` (alta, media, baixa), `evidencia`, `receita` (caminho em `receitas/` ou `null`), `possivel_decisao[]` (trechos do CLAUDE.md do cliente que podem ser a regra por trás da "falha") |
| `funil` | `saidas_para_outros_enderecos[]`: destino, tipo, links, páginas de origem, botões mais usados (hipótese H) |

Status de página `999` = o robots.txt do site pediu para não ler; `0` = falha de rede.

## Limites conhecidos
- Só lê HTML recebido: conteúdo montado por JavaScript e scripts de outros endereços não aparecem.
- Detecção de medição, preço e prova social é por padrões de texto: pode errar para mais ou para menos.
- "Possível decisão do cliente" é por palavras-chave nas regras do cliente: pode acusar de mais ou de menos. Quem decide é uma pessoa.
