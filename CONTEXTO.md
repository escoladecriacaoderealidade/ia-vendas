# CONTEXTO DO PROJETO — IA Vendas

> Documento de passagem para continuar o trabalho direto do VS Code. Atualizado em **05/11/2026**.
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
`coletor.py` (uma página) · `site.py` (site inteiro, robots, sitemap, llms.txt) · `repositorio.py` (lê CLAUDE.md, decisões, pendências, código de SEO/medição) · `achados.py` (separa "possível decisão do cliente" de lacuna) · `funil.py` (saídas para outros endereços, hipótese H) · `relatorio.py` · `cli.py`. 37 testes (uma vez um deles falhou numa rodada e passou sozinho nas três seguintes: `test_http_respeita_robots...`; I: intermitente, causa não investigada) (`python -m pytest`).

Comando principal (no PowerShell do VS Code, **não** no `>>>` do Python):
```
python -m ia_vendas analisar --url https://escoladecriacaoderealidade.com.br --saida resultado
```
Opções: `--dir PASTA` (repetível, lê site estático em disco), `--repo PASTA` (lê o repositório do cliente), `--max-paginas`, `--intervalo`. Identifica-se como `IAVendasBot`, respeita robots.txt, 1 s entre pedidos. Passo a passo para Windows: `docs/como-rodar-no-windows.md`. Formato da saída: `docs/formato-analise.md`.

**Robô diário:** tarefa agendada `trig_01WxmNnSKco9gsvbbLyh9H4U`, todo dia 06:56 (Brasília). Só leitura; escreve apenas no documento `monitor-mecanismos-venda` do Projeto Claude "IA Vendas"; só alerta em mudança de alto impacto. **Primeira execução ocorreu em 04/11/2026 e funcionou** (promoveu duas regras a V; ver seção 6).

**Documentos vivos (no Projeto Claude "IA Vendas", pasta `claude/`):** `diagnostico-inicial-2026-11-03`, `enquanto-auditoria-2026-11-03`, `monitor-mecanismos-venda` (regras + changelog, **mantido pelo robô**), `guia-de-publicacao-e-recuperacao-2026-11-03` (Etapas 0–6 e tabela de retorno), `ia-vendas-arquitetura-2026-11-03` (aponta para `docs/arquitetura.md`). Painel visual: artefato "Painel" no Claude (identificador `9c57e652-2d49-4e5d-b6fc-59aa89852b0f`); pode estar desatualizado em relação à seção 3.

**Receitas** (`receitas/`): compartilhamento Open Graph/Twitter, canal de anúncios nas estatísticas, visita de página e cliques, canal do cadastro.

---

## 3. Estado dos pull requests e das publicações (05/11/2026)

Regra do projeto: **nada vai direto na `main`; tudo por pull request que o Carlos revisa.** Registro completo de cada deploy e ponto de volta: `C:\Users\Cliente\Documents\backups-ia-vendas\deploys-atuais-2026-11-05.md` (fora dos repositórios; o Carlos guarda cópia em HD externo).

**No ar em 05/11/2026 (V, conferido por consulta ao site e ao banco):**

| Site | Versão / commit | O que entrou |
|---|---|---|
| Escola (`escoladecriacaoderealidade.com.br`) | `main` 480f942 | Preços só na página de cada livro (D), botão "Comprar no Enquanto", tags de compartilhamento, correção das capas em "outras obras", botão X do menu no computador, **medição anônima (`medir.js`) em 21 páginas**. |
| Enquanto / Estuda | 4.113.2 (`main` 9670403) | Canal do fbclid = `meta`; **`/api/visita` + tabela `visitas`**; origens aceitas: Escola, `www.enquantoestuda.com.br`, `estuda.` e `enquanto.escoladecriacaoderealidade.com.br`; política de privacidade com MEI (só CNPJ) e "Páginas públicas"; contato = `escoladecriacaoderealidade@gmail.com`. |
| Imitação de Cristo (API e site) | `main` 43f7411 | Canal de origem do cadastro (`users.metadata`, relatório `/v1/admin/reports/channels`); Política e Termos com o MEI como titular. |
| Supabase `enquanto-br` | `banco-supabase-20.sql` rodado | Tabela `visitas` (RLS ligado, sem políticas) e função `visitas_resumo`. Visitas reais da Escola e do Estuda gravadas e conferidas pelo Carlos. |

**Repositório ia-vendas:** #1 (Fase 1), #2 (falso Google Analytics por pasta de cache) e #3 (receita: fbclid = `meta`) estão mesclados.

**Pull requests antigos que devem ser fechados, se ainda abertos (I, não conferi):** Escola #1, #2 e #5 (foram refeitos e substituídos; o refeito do `medir.js` é o #9, mesclado). Não mesclar nenhum deles: estão sobre uma base velha e apagariam preços, capas e menu.

**Buscadores (V, fotos do Carlos em 05/11/2026):** Google Search Console e Bing Webmaster têm os **5 endereços** cadastrados e verificados: `escoladecriacaoderealidade.com.br`, `app.escoladecriacaoderealidade.com.br`, `enquanto.escoladecriacaoderealidade.com.br`, `www.enquantoestuda.com.br` e `ia-consciencia-web.vercel.app` (endereço técnico do Vercel). Escola e app foram verificados por **arquivo HTML** `googlefdab9d4b08a75bdb.html` (a tag `w5Csnr…` da Escola é de outra conta Google). **NÃO REMOVER esse arquivo de nenhum site**: o Google perde a verificação. Sitemaps lidos com sucesso: Escola (Google leu 20 em 31/10; no ar são 21; Bing leu 21), `enquanto.` (137), `www.enquantoestuda.com.br` (índice com `sitemap-estuda.xml` 134 + `sitemap-concursos.xml`, que cresce por dia: Google 403 em 03/11, no ar 464 em 05/11). O `app.` não tem sitemap (404) e o envio de teste que o Carlos fez deu erro esperado (remover o registro). Os dados de busca dos endereços novos só aparecem 1 a 2 dias depois; o `www.enquantoestuda.com.br` tinha 6 cliques de pesquisa em 24/10–03/11 (volume muito baixo: qualquer conclusão sobre palavras e público ainda é H). O Bing tem o relatório "Desempenho da IA (BETA)" no menu (existência V; conteúdo não verificado).

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

**Ordem de publicação que funcionou em 05/11 (V):** banco → API → site, um por vez, conferindo o site no ar e a tabela entre um e outro. Antes de cada deploy: copiar o site que está no ar para `backups-ia-vendas`, construir, comparar com o que está no ar ignorando datas e versão, mostrar ao Carlos e esperar "pode publicar". A Escola é publicada a partir da pasta limpa `Documents\GitHub\escola-publicar` (com `.vercel` copiado), não da pasta de trabalho antiga. A prévia do Vercel (sem `--prod`) fica atrás de login: serve só para o Carlos olhar, não para teste automático nem de medição (a origem dela não é aceita).

---

## 5. Pendências, em ordem

### Carlos (ações dele)
1. **Revisar com o contador os textos de privacidade** (MEI só com o CNPJ como titular; coleta anônima de visitas; contato novo). Já estão no ar (texto aprovado por ele em 05/11).
2. **Copiar a pasta `backups-ia-vendas` de novo para o HD externo** (cresceu depois da última cópia: backups do Enquanto 4.113.0 e 4.113.1, registros de deploy) e guardar cópia dos livros completos (`enquanto-app\biblioteca\`, `enquanto\privado\`; **não estão no GitHub de propósito**, D).
3. **Fechar no GitHub os PRs antigos da Escola** (#1, #2, #5), se ainda abertos.
4. Conferir a tela "Quem publica o app" dentro do app (deve mostrar o e-mail novo; o texto da INFLOW como publicadora foi mantido por decisão dele, D).
5. Se quiser o mesmo e-mail na loja: mudar o contato no painel do Google Play (não está no repositório).
6. **Search Console e Bing:** cadastro, verificação e sitemaps feitos em 05/11 (ver seção 3). Falta: (a) reenviar o `sitemap.xml` da Escola no Google para ele passar de 20 para 21 páginas; (b) remover o envio com erro de sitemap do `app.`; (c) **a partir de 06/11**, em cada propriedade: Desempenho → Exportar → Baixar CSV (consultas e páginas), e também o relatório Indexação → Páginas (o que o Google aceitou ou recusou), e entregar os arquivos ao Claude (sem chaves); (d) Google Cloud → Público → **Publicar app** (login Google do Imitação de Cristo).
7. Decidir (D) **antes de qualquer campanha**: ver seção 6 (Merchant Center).
8. Definir primeiros clientes além dos sites dele e, quando existirem, contas de anúncios (Google, Bing, Meta) com quem dá acesso e teto de gasto.

### Claude / desenvolvimento
0. **Ordem acordada em 05/11 (D do Carlos) para chegar ao modelo de máxima precisão:** (1) dados reais de busca (Search Console e Bing: em andamento) → (2) motor de recomendações priorizadas (impacto × esforço) → (3) ligar o robô diário às recomendações (antes, 2 semanas de execuções estáveis) → (4) funil completo até o pagamento (qual canal vende, não só traz visita) → (5) verificações novas: velocidade e celular (PageSpeed/Lighthouse), links quebrados, redirecionamentos, títulos duplicados, conteúdo fraco, indexação real, dados estruturados por tipo (livro, curso, app, oferta), robôs de IA permitidos, perfil de empresa local → (6) vários clientes e painel; campanhas só depois, com aprovação e teto. Cada etapa só avança quando a anterior estiver medida e conferida. Ninguém garante primeira página (regra 6): o sistema maximiza elegibilidade e qualidade e mede a posição real.
0b. **A investigar (H, não verificado):** (a) a Escola abre igual com e sem `www` (ambos 200, sem redirecionamento): conferir o canônico e o risco de duplicidade; (b) o endereço técnico `ia-consciencia-web.vercel.app` está cadastrado nos buscadores: ver se o Google guardou páginas dele que deveriam estar só em `app.`; (c) falso alarme do detector "política de privacidade não encontrada" na Escola (ela aponta para a política do Enquanto): ensinar o detector.
1. **Testar o canal de cadastro do Imitação de Cristo** no relatório `/v1/admin/reports/channels` com um cadastro real (ainda não verificado no ar).
2. Rodar de novo a análise **pela internet no computador do Carlos** (Escola, Enquanto Estuda, app), com `--repo`, para ver o efeito das mudanças de hoje (preços, medição) nos achados.
3. Decidir com o Carlos se o resumo de visitas (`visitas_resumo`) entra no relatório da Fase 1. Ligar o relatório ao robô diário só com aprovação dele (hoje o robô só atualiza o monitor de regras).
4. **Fase 2:** base de regras com histórico; robô estável por 2 semanas; resumo semanal.
5. **Fase 3:** motor de recomendações priorizadas (impacto × esforço), grafo de funil completo, receitas catalogadas.
6. Fases 4–5 (painel, vários clientes, campanhas com aprovação e teto) — ver `docs/arquitetura.md`.
7. Pequenas: `medir.js` envia evento de clique também para links de rodapé (privacidade) — ruído menor, distinguível pelo destino; os relatórios existentes não contam a tabela `visitas` (regra 8 do CLAUDE.md; I, pelo desenho de tabela à parte). Os documentos internos `enquanto/play/ficha-da-loja.md` e `enquanto/docs/android-play.md` ainda citam o e-mail antigo da INFLOW.

---


## 6. O que o robô já confirmou (V, 04/11/2026; não revisto em 05/11) — leia antes de planejar anúncios

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
- Um teste que "deu zero" pode ser o teste errado: a medição de visitas descarta em silêncio origens fora da lista, e testei por um endereço que não estava nela. Antes de culpar o código, conferir pelo endereço oficial (`canonical`).
- Branch de PR antigo (Escola #1/#2/#5) ficou sobre base velha: mesclar apagaria trabalho já publicado. Ao refazer, partir da `main` atual e conferir que só mudaram as linhas esperadas (`git diff --stat` e linhas removidas = 0).
- Colar o **caminho** de um arquivo no corpo do PR em vez do texto dele (aconteceu no Escola #5). Abrir o arquivo e copiar o conteúdo.
- A prévia do Vercel exige login: o teste automático recebe a página de login (200) e engana. Dizer isso ao Carlos em vez de afirmar que a prévia funciona.
