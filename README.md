# IA de Vendas

IA que analisa o site e o modelo de venda de **qualquer cliente**, encontra os funis reais de venda (da marca e de cada produto), compara com as regras dos mecanismos de venda (Google, Bing/Copilot, ChatGPT e outros), recomenda a divulgação e o público com grau de certeza, e vigia todo dia se essas regras mudaram.

Os sites do Carlos Farias são os **casos de teste**: Escola de Criação de Realidade, Enquanto / Enquanto Estuda e Imitação de Cristo.

## Situação (03/11/2026)
Fase 0 concluída: três casos auditados, medição própria nos três (em pull requests, nada publicado), base de regras inicial e robô diário agendado. **Ainda não há código do produto neste repositório.** Veja o roteiro em [docs/arquitetura.md](docs/arquitetura.md).

## O que há aqui
| Pasta | Conteúdo |
|---|---|
| `docs/arquitetura.md` | Estrutura proposta do produto, módulos, modos de operação, roteiro e decisões pendentes |
| `receitas/` | Receitas reutilizáveis: o que verificar, critério de "certo", como corrigir. Quatro já foram feitas em casos reais |
| `CLAUDE.md` | Regras de trabalho para quem (pessoa ou IA) mexer neste repositório |

## Onde ficam os documentos vivos
Os relatórios que mudam com frequência ficam no **Projeto "IA Vendas"** no Claude, para existir uma só cópia:
- `diagnostico-inicial-2026-11-03` — diagnóstico dos três casos
- `enquanto-auditoria-2026-11-03` — auditoria do repositório do Enquanto
- `monitor-mecanismos-venda` — base de regras e changelog, **atualizado todo dia pelo robô**
- `guia-de-publicacao-e-recuperacao-2026-11-03` — passo a passo para publicar e voltar atrás

## Repositórios relacionados
`escola-de-criacao-de-realidade`, `enquanto`, `ia-consciencia` (todos na organização `escoladecriacaoderealidade`).
