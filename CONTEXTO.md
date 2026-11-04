# CONTEXTO DO PROJETO — IA Vendas

> Documento de passagem para continuar o trabalho direto do VS Code. Atualizado em **04/11/2026**.
> Dono: **Carlos Farias** (José Carlos Rosa Farias), Santa Maria/RS. Não é programador: fale em português do Brasil, simples, passo a passo, com o caminho exato dos menus. Ele manda fotos da tela.
> Se você é um assistente de IA lendo isto: **leia inteiro, depois leia `CLAUDE.md` (regras)**, antes de mudar qualquer coisa. Os estatutos usados aqui: **V** verificado na fonte (com data) · **R** reportado por terceiros · **I** inferido · **H** hipótese · **D** decisão do cliente.

---

## 1. O que é

Uma IA que serve para **qualquer site ou modelo de venda**: lê o negócio, mapeia os funis reais (da marca e de cada produto), compara com as regras dos mecanismos de venda (Google, Bing/Copilot, ChatGPT e outros), recomenda divulgação e público com grau de certeza, e **vigia todo dia** se essas regras mudaram. Os sites do Carlos são os **casos de teste**:

| Caso | Endereço | Repositório (GitHub `escoladecriacaoderealidade/…`) | Pasta no computador do Carlos |
|---|---|---|---|
| Escola de Criação de Realidade (vitrine de livros) | escoladecriacaoderealidade.com.br | `escola-de-criacao-de-realidade` | `C:\Users\Cliente\Documents\GitHub\escola-de-criacao-de-realidade` |
| Enquanto / Enquanto Estuda (app de leitura em áudio, assinaturas) | enquanto.escoladecriacaoderealidade.com.br e enquantoestuda.com.br (mesmo site) | `enquanto` (código em `enquanto/`) | `C:\Users\Cliente\Documents\GitHub\enquanto-app` (ligada ao repositório em 04/11/2026) |
| Imitação de Cristo (app de IA, planos pagos) | app.escoladecriacaoderealidade.com.br | `ia-consciencia` | `C:\Users\Cliente\Documents\GitHub\ia-consciencia` |
| **Este projeto** | — | `ia-vendas` | `C:\Users\Cliente\Documents\GitHub\ia-vendas` |

Cada caso tem o próprio `CLAUDE.md` com regras do dono. **Leia o do caso antes de recomendar qualquer coisa** (decisão deliberada ≠ lacuna; ex.: o site da Escola não mostra preço **de propósito**).

---

## 2. O que existe hoje

**Código (Fase 1, Python só com biblioteca padrão):** `ia_vendas/`
`coletor.py` (uma página) · `site.py` (site inteiro, robots, sitemap, llms.txt) · `repositorio.py` (lê CLAUDE.md, decisões, pendências, código de SEO/medição) · `achados.py` (separa "possível decisão do cliente" de lacuna) · `funil.py` (saídas para outros endereços, hipótese H) · `relatorio.py` · `cli.py`. 36 testes (`python -m pytest`).

Comando principal (no PowerShell do VS Code, **não** no `>>>` do Python):
```
python -m ia_vendas analisar --url https://escoladecriacaoderealidade.com.br --saida resultado
```
Opções: `--dir PASTA` (repetível, lê site estático em disco), `--repo PASTA` (lê o repositório do cliente), `--max-paginas`, `--intervalo`. Identifica-se como `IAVendasBot`, respeita robots.txt, 1 s entre pedidos. Passo a passo para Windows: `docs/como-rodar-no-windows.md`. Formato da saída: `docs/formato-analise.md`.

**Robô diário:** tarefa agendada `trig_01WxmNnSKco9gsvbbLyh9H4U`, todo dia 06:56 (Brasília). Só leitura; escreve apenas no documento `monitor-mecanismos-venda` do Projeto Claude "IA Vendas"; só alerta em mudança de alto impacto. **Primeira execução ocorreu em 04/11/2026 e funcionou** (promoveu duas regras a V; ver seção 6).

**Documentos vivos (no Projeto Claude "IA Vendas", pasta `claude/`):** `diagnostico-inicial-2026-11-03`, `enquanto-auditoria-2026-11-03`, `monitor-mecanismos-venda` (regras + changelog, **mantido pelo robô**), `guia-de-publicacao-e-recuperacao-2026-11-03` (Etapas 0–6 e tabela de retorno), `ia-vendas-arquitetura-2026-11-03` (aponta para `docs/arquitetura.md`). Painel visual: artefato "Painel" no Claude (identificador `9c57e652-2d49-4e5d-b6fc-59aa89852b0f`); pode estar desatualizado em relação à seção 3.

**Receitas** (`receitas/`): compartilhamento Open Graph/Twitter, canal de anúncios nas estatísticas, visita de página e cliques, canal do cadastro.

---

## 3. Estado dos pull requests (04/11/2026) — NADA disto está publicado nos sites

Regra do projeto: **nada vai direto na `main`; tudo por pull request que o Carlos revisa.**

| Repositório | PR | Situação | O que faz |
|---|---|---|---|
| escola | #3 `trabalho-local-aplicativos` | **mesclado** | Salvou no GitHub o trabalho que só existia no computador (página Aplicativos, visual novo, PWA, 39 arquivos). |
| escola | #1 `melhorias-medicao-e-descoberta` | aberto | Tags og:image/og:site_name/twitter em todas as páginas + logo no Organization. **Precisa ser refeito sobre o #3** (conflitos esperados em `index.html`, páginas de livros geradas, `sitemap.xml`, `tools/gerar_paginas_livros.py`). |
| escola | #2 `medicao-propria` (rascunho) | aberto | `medir.js` + `tools/medicao.py`. **Também precisa ser refeito sobre o #3.** Depende do endpoint do Enquanto #2. |
| enquanto | #3 e #4 | **mesclados** | Removeu a cópia antiga da raiz (136 arquivos), reforçou `.gitignore` (biblioteca/, enquanto/site/, enquanto/privado/, .env), adicionou `COMO-PUBLICAR.md`. |
| enquanto | #1 `canal-anuncios-medicao` | aberto | `canal()` reconhece gclid/msclkid/fbclid/utm_source. |
| enquanto | #2 `medicao-visitas-paginas` (rascunho) | aberto | `api/visita.js`, tabela `visitas` (SQL `enquanto/docs/banco-supabase-20.sql`), texto de privacidade "Páginas públicas". **Exige rodar o SQL no Supabase antes do deploy.** |
| ia-consciencia | #1 `registra-canal-cadastro` | aberto | Guarda o canal de origem do cadastro (`users.metadata`, sem migration) + relatório `/admin/reports/channels`. |
| ia-vendas | #1 `fase-1-coletor` | aberto | O código da Fase 1 e este documento. **Mesclar primeiro** (ver seção 5, passo 1). |

Confira sempre o estado real antes de agir (GitHub → aba *Pull requests*). Esta tabela envelhece.

---

## 4. Como o Carlos publica cada coisa (resumo; completo no guia do Projeto)

**Ordem sempre: banco → API → site.**
- **Escola (Vercel, projeto `escola-de-criacao-de-realidade`):** da pasta do projeto, `npx vercel@62.5.0 deploy --prod --yes`. Publicação é manual por CLI (sem integração Git): **mesclar no GitHub não publica nada.**
- **Enquanto (Vercel, projeto `enquanto`):** `python pwa/build.py X.Y.Z` e depois `npx vercel@62.5.0 deploy --prod --yes` dentro de `enquanto/site`.
- **Imitação de Cristo — API (Railway, projeto `supportive-fulfillment`):** publica sozinho ao fazer merge na `main` (~2 min). Conferir `https://ia-consciencia-production.up.railway.app/v1/health`.
- **Imitação de Cristo — site (Vercel, projeto `ia-consciencia-web`):** `npm run export:web` em `apps/mobile`, copiar `dist` para `C:\deploy-web`, `vercel --prod` **somente dentro de `C:\deploy-web`** (nunca na raiz do repositório).
- **Banco (Supabase):** SQL colado em *SQL Editor → New query → Run*.

**Voltar atrás:** Vercel → projeto → *Deployments* → ⋯ na versão antiga → *Promote to Production* (ou *Instant Rollback*). Railway → *Deployments* → versão antiga → *Redeploy*. Código: branch `backup-2026-11-03` existe nos 3 repositórios de cliente (commits: Escola `36a4441b19`, Enquanto `99fbef1bc8`, ia-consciencia `aed398d888`).

**Ordem sugerida de publicação (I — conferir nos corpos dos PRs):** (1) Enquanto #1 · (2) SQL `banco-supabase-20` → Enquanto #2 · (3) ia-consciencia #1 (API, depois site) · (4) Escola #1 refeito · (5) Escola #2 refeito (só depois do Enquanto #2 no ar, porque envia visitas para ele). Um por vez, conferindo o site entre um e outro.

---

## 5. Pendências, em ordem

### Carlos (ações dele)
1. **Revisar e mesclar `ia-vendas` PR #1** e depois, no VS Code: `git checkout main` e `git pull`.
2. **Anotar os deploys atuais** (para poder voltar): Vercel (escola, enquanto, ia-consciencia-web) = endereço do deploy marcado *Production*; Railway `supportive-fulfillment` → serviço → *Deployments* → o *ACTIVE*. Guardar no guia do Projeto. *(Em 04/11 ele já viu o da Escola: commit `36a4441`, 31/out; faltam os outros.)*
3. **Guardar cópia de segurança dos livros completos** (`enquanto-app\biblioteca\`, `enquanto\privado\`): **não estão no GitHub de propósito** (D) e só existem no computador. Copiar para um HD externo ou Drive privado.
4. Atualizar a pasta local da Escola com segurança depois do #3 (não usar `git pull` com mudanças soltas): renomear a pasta antiga, clonar de novo, copiar `.env.local` e a pasta `.vercel`. **O Claude passa o passo a passo na hora.**
5. Rodar `banco-supabase-20.sql` no Supabase **só quando for publicar o Enquanto #2**.
6. Revisar o texto de privacidade com o contador (CNPJ do MEI × INFLOW), antes de publicar medição de visitas.
7. Google Search Console e Bing Webmaster: cadastrar os sites e os sitemaps; Google Cloud → Público → **Publicar app** (login Google do Imitação de Cristo).
8. Decidir (D) **antes de qualquer campanha**: ver seção 6 (Merchant Center).
9. Definir primeiros clientes além dos sites dele e, quando existirem, contas de anúncios (Google, Bing, Meta) com quem dá acesso e teto de gasto.

### Claude / desenvolvimento
1. **Refazer Escola PR #1 e #2 por cima do #3 mesclado** (primeira coisa a fazer numa sessão nova).
2. Rodar a análise **pela internet no computador do Carlos** (sessões na nuvem não alcançam sites de fora): Escola, Enquanto Estuda, app; com `--repo` para ver os achados de "possível decisão" (preço etc.); medir tempo em site grande.
3. Ligar o relatório da Fase 1 ao robô diário (hoje o robô só atualiza o monitor de regras).
4. **Fase 2:** base de regras com histórico; robô estável por 2 semanas; resumo semanal.
5. **Fase 3:** motor de recomendações priorizadas (impacto × esforço), grafo de funil completo, receitas catalogadas.
6. Fases 4–5 (painel, vários clientes, campanhas com aprovação e teto) — ver `docs/arquitetura.md`.
7. Pequenas: `medir.js` da Escola envia evento de clique para links de rodapé (privacidade) — ruído menor, distinguível pelo destino; confirmar que os relatórios existentes não ficam distorcidos (regra 8 do CLAUDE.md).

---

## 6. O que o robô já confirmou (V, 04/11/2026) — leia antes de planejar anúncios

- **Merchant Center (política oficial "Unsupported Shopping content"):** e-books/livros digitais **não** são permitidos em anúncios **Shopping** (valem listagens gratuitas); conteúdo digital com assinatura recorrente não é aceito como pagamento recorrente. Implicação (I): livros em e-book da Escola e assinaturas mensais do Enquanto/Imitação de Cristo **não** devem ir para campanha Shopping. Falta verificar a situação de apps e de audiolivros na prática. **Precisa de decisão do Carlos.**
- **Anúncios no AI Mode (Google, 28/10/2026):** ativos em 10 países; **Brasil ainda não**, previsto "in Q4 2026". Ação sugerida: preparar dados estruturados, feeds e conversões antes.
- **Ainda R (não confirmado na fonte):** ChatGPT Ads no Brasil (datas divergentes; página oficial não abriu), AI Max/Copilot ads/Copilot Checkout da Microsoft, UCP, ACP. O robô promove ou corrige uma regra por dia.

---

## 7. Como trabalhar neste repositório

- Abrir `C:\Users\Cliente\Documents\GitHub\ia-vendas` no VS Code. Terminal = PowerShell (`PS C:\...>`). Se aparecer `>>>`, saiu para o Python: digitar `exit()`.
- Testes: `python -m pytest` (rodar antes e depois e comparar).
- Código só com biblioteca padrão do Python (`pip` falha neste computador por certificado).
- Fluxo de mudança: `git checkout -b nome-do-branch` → editar → `git add arquivo` (arquivos nomeados, **nunca `git add -A`** em pastas de cliente) → `git commit` → `git push -u origin nome-do-branch` → abrir o link que o push mostra para criar o PR → Carlos revisa e mescla.
- **Antes de mexer num repositório de cliente:** registrar o commit da `main` e criar `backup-AAAA-MM-DD` (CLAUDE.md, "Ponto de recuperação").
- Limites do ambiente **de nuvem** (não valem no VS Code do Carlos): sem acesso a sites externos pelo shell, sem criar tags/repositórios, GraphQL do GitHub bloqueado (usar REST). No computador dele esses limites não existem; **tags de recuperação podem ser criadas por lá**.
- Segredos: só nos cofres (Vercel, Railway, Supabase, variáveis de ambiente). **Nunca pedir nem colar chaves no chat.**
- Textos para clientes: nunca prometer resultado, cura nem "grátis para sempre"; no Escola, nunca copiar preços para o site.
- Privacidade (LGPD): medição anônima, sem cookies de publicidade, respeitando "Não rastrear"; guardar só o **tipo** de canal, nunca gclid/msclkid/fbclid nem dados pessoais; mudou o que se coleta → atualizar a política **antes** de publicar.

---

## 8. Lições já pagas (não repetir)

- Eu afirmei que a Escola não tinha JSON-LD/robots/llms/sitemap e que deveria mostrar preço: **errado** (a Escola tem tudo isso e o preço é decisão do dono). Leia o CLAUDE.md do cliente primeiro.
- "21 páginas" em um PR eram 20: **confira números citados**.
- O site da Escola no ar tinha trabalho que **não estava no GitHub** (descoberto por uma execução real do Carlos). Antes de qualquer PR, comparar o que está no ar com a `main`.
- Comentário no fim da linha do `.gitignore` vira parte do padrão e desliga a proteção: **comentário em linha própria** e testar com `git add -A -n`.
- Quebras de linha do Windows geram "modified" falso (`core.autocrlf true` na pasta ligada).
- `vercel --prod` rodado na pasta errada criou projeto errado no passado: só dentro da pasta indicada de cada projeto.
