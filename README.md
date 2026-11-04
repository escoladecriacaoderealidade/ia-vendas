# IA de Vendas

IA que analisa o site e o modelo de venda de **qualquer cliente**, encontra os funis reais de venda (da marca e de cada produto), compara com as regras dos mecanismos de venda (Google, Bing/Copilot, ChatGPT e outros), recomenda a divulgação e o público com grau de certeza, e vigia todo dia se essas regras mudaram.

Os sites do Carlos Farias são os **casos de teste**: Escola de Criação de Realidade, Enquanto / Enquanto Estuda e Imitação de Cristo.

## Situação (03/11/2026)
Fase 0 concluída (três casos auditados, medição própria nos três em pull requests, base de regras inicial e robô diário agendado). **Fase 1 em pull request:** o coletor de site, o leitor de repositório, os achados e o relatório já funcionam e têm 35 testes. Veja o roteiro em [docs/arquitetura.md](docs/arquitetura.md).

## Como usar
Passo a passo para Windows: [docs/como-rodar-no-windows.md](docs/como-rodar-no-windows.md). Só precisa do Python 3 (sem instalar nada):

```
python -m ia_vendas analisar --url https://exemplo.com.br --repo ../pasta-do-repositorio-do-cliente --saida resultado
```

Gera `resultado/analise.json` (dados, ver [docs/formato-analise.md](docs/formato-analise.md)) e `resultado/relatorio.md` (relatório em português no formato do diagnóstico inicial).

- `--dir PASTA` analisa os arquivos de um site estático em disco, sem rede (a `--url` continua sendo o endereço real). Pode repetir `--dir` para sites montados em camadas: vale a primeira pasta que tiver o arquivo.
- Pela internet o coletor se identifica como `IAVendasBot`, **respeita o robots.txt**, espera 1 segundo entre pedidos e lê no máximo 60 páginas (`--max-paginas`).
- **Atenção:** as sessões do Claude não alcançam sites de fora (bloqueio de rede). Rode no seu computador ou use `--dir`.
- Testes: `python -m pytest`

## O que há aqui
| Pasta | Conteúdo |
|---|---|
| `ia_vendas/` | O código: `coletor.py` (uma página), `site.py` (o site inteiro), `repositorio.py`, `achados.py`, `funil.py`, `relatorio.py`, `cli.py` |
| `tests/` | 36 testes automáticos (sites de exemplo, servidor local, repositório de exemplo) |
| `docs/arquitetura.md` | Estrutura proposta do produto, módulos, modos de operação, roteiro e decisões pendentes |
| `docs/formato-analise.md` | O que há dentro do `analise.json` |
| `receitas/` | Receitas reutilizáveis: o que verificar, critério de "certo", como corrigir. Quatro já foram feitas em casos reais |
| `CONTEXTO.md` | **Comece por aqui:** estado atual, pull requests, como publicar, pendências em ordem, lições aprendidas |
| `CLAUDE.md` | Regras de trabalho para quem (pessoa ou IA) mexer neste repositório |

## Onde ficam os documentos vivos
Os relatórios que mudam com frequência ficam no **Projeto "IA Vendas"** no Claude, para existir uma só cópia:
- `diagnostico-inicial-2026-11-03` — diagnóstico dos três casos
- `enquanto-auditoria-2026-11-03` — auditoria do repositório do Enquanto
- `monitor-mecanismos-venda` — base de regras e changelog, **atualizado todo dia pelo robô**
- `guia-de-publicacao-e-recuperacao-2026-11-03` — passo a passo para publicar e voltar atrás

## Repositórios relacionados
`escola-de-criacao-de-realidade`, `enquanto`, `ia-consciencia` (todos na organização `escoladecriacaoderealidade`).
