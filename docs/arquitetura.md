# IA de Vendas — estrutura proposta (rascunho, atualizado em 03/11/2026)

Objetivo: uma IA que serve para qualquer site ou modelo de venda. Os sites do Carlos são os casos de teste. Este rascunho nasceu do que foi feito de verdade nos três casos (Escola, Enquanto/Estuda, Imitação de Cristo) e das peças que já existem nos repositórios. Nada aqui está construído ainda, exceto o que está marcado "já existe".

## 1. O que a IA faz, em ordem
1. **Lê o negócio**: site, páginas, código (quando houver acesso), regras e decisões do dono. Separa *decisão deliberada* de *lacuna* (aprendizado do caso da Escola: não mostrar preço era regra do dono, não falha).
2. **Mapeia os funis**: do primeiro contato até a compra, por marca e por produto. Cada passo é uma página, botão, app ou checkout, com o que se mede ali.
3. **Compara com as regras dos mecanismos** (Google, Bing/Copilot, ChatGPT, outros): o que está elegível, o que reprova, o que falta.
4. **Recomenda**: divulgação, canais, público e ordem de execução, com evidência e grau de certeza.
5. **Executa o que é seguro** (pull request de código, texto, dados estruturados) e **pede aprovação** para o que gasta dinheiro ou publica.
6. **Vigia todo dia** se os mecanismos mudaram e reabre as recomendações afetadas.

## 2. Módulos
| Módulo | Função | Situação |
|---|---|---|
| Coletor de site | Busca páginas, extrai título, descrição, JSON-LD, links, botões, formulários, etiquetas de medição, robots/sitemap/llms.txt | **Fase 1 pronta** (`ia_vendas/coletor.py`, `site.py`); testado em pasta local e servidor local, ainda não em sites reais pela internet |
| Leitor de repositório | Lê CLAUDE.md, decisões, pendências, código de SEO e de medição | **Fase 1 pronta** (`ia_vendas/repositorio.py`) |
| Mapa de funil | Grafo de passos (página → botão → app → checkout) + eventos medidos + quebras | Versão simples pronta (`funil.py`: saídas para outros endereços, hipótese H); o grafo completo fica para a Fase 3 |
| Medição própria padrão | Visita, clique, canal de origem, sem cookies, respeita "Não rastrear" | **Já existe** no Enquanto e no Estuda (eventos); em pull request para a Escola (visitas) e para o Imitação de Cristo (canal do cadastro) |
| Base de regras dos mecanismos | Regras versionadas, cada uma com fonte, data, confiança | Documento inicial criado (`monitor-mecanismos-venda`, no Projeto), ainda em estatuto R |
| Robô diário | Coleta fontes, compara, classifica impacto, atualiza a base, alerta | Tarefa agendada criada: todo dia às 06:56 (Brasília), primeira execução em 04/11/2026; ainda não testada |
| Motor de recomendações | Cruza funil × regras × dados e propõe ações priorizadas | A construir |
| Receitas | Cada ajuste vira uma receita reutilizável: o que verificar, critério de "certo", como corrigir | Quatro prontas em [`receitas/`](../receitas/README.md) |
| Executor | Gera pull requests ou instruções; campanhas só com aprovação e limite de gasto | Pull requests: já fazemos; campanhas: não |
| Guardiões | Sem promessas de resultado, LGPD/consentimento, políticas de anúncios, regras do cliente | Começam em [`CLAUDE.md`](../CLAUDE.md); formalizar |

## 3. Estatuto de cada afirmação (adaptado do projeto Imitação de Cristo)
O projeto Imitação de Cristo já distingue estatutos epistemológicos (P/E/H/D/F). Para vendas, o equivalente:
- **V — verificado na fonte oficial** (data da verificação).
- **R — reportado por terceiros** (blog, notícia), ainda não confirmado na fonte.
- **I — inferido** do código, dos dados ou do conteúdo do site.
- **H — hipótese** (público, intenção de busca), a validar com Search Console ou dados reais.
- **D — decisão do cliente** (ex.: "não mostrar preço no site"; "a voz Faber não será usada").
Toda recomendação carrega o estatuto das afirmações em que se apoia.

## 4. Dados (esboço)
`clientes` → `ativos` (site, app, repositório) → `paginas` → `passos_de_funil` → `eventos_agregados` (visitas, cliques, cadastros, pagamentos, por canal).
`regras` (mecanismo, texto, fonte, estatuto, verificada_em, vale_de, vale_ate) → `mudancas_de_regra` (o que mudou e quando).
`recomendacoes` (cliente, ativo, regra, evidência, impacto, esforço, estado: nova/aprovada/feita/descartada) → `execucoes` (PR, link, resultado).
Reaproveitar do repositório ia-consciencia: banco PostgreSQL/Supabase, busca em documentos (RAG), memória, adaptador de modelos (OpenAI/Anthropic/determinístico para teste), planos e cobrança, relatórios de administrador e o padrão de testes.

## 5. Modos de operação (segurança)
1. **Recomendar** (padrão): só leitura. Entrega relatório.
2. **Propor mudança**: abre pull request; nada publica sozinho.
3. **Campanha**: cria rascunho; qualquer gasto exige aprovação humana e teto diário configurado. A IA nunca aumenta orçamento sozinha.

## 6. Roteiro
- **Fase 0 (feita em 03/11/2026)**: três casos auditados, cinco pull requests abertos (nenhum publicado; dois em rascunho), base de regras inicial, robô diário agendado, repositório `ia-vendas` criado com regras e receitas.
- **Fase 1 (em pull request, 03/11/2026)**: coletor de site, leitor de repositório, achados (separando decisão deliberada de lacuna), funil simples e relatório em Markdown, com saída padronizada em JSON. Validada nos clones da Escola, do Enquanto Estuda e do Imitação de Cristo; os achados bateram com a auditoria manual. **Falta** rodar em sites reais pela internet (no computador do Carlos), medir tempo em sites grandes e ligar o relatório ao robô diário.
- **Fase 2**: base de regras com histórico, robô diário estável por 2 semanas, resumo semanal.
- **Fase 3**: motor de recomendações priorizadas (impacto × esforço) e receitas catalogadas.
- **Fase 4**: painel e vários clientes; cobrança.
- **Fase 5**: execução em campanhas com aprovação e teto de gasto.

## 7. Decisões
**Decidido em 03/11/2026:** o produto mora num repositório novo, `ia-vendas` (D).

**Dependem do Carlos:**
1. Quem são os primeiros clientes além dos sites do Carlos.
2. Contas de anúncios (Google, Bing, Meta): quando existirem, quem dá acesso e com que limite.
3. Modelo de preço do produto.
4. Search Console e Bing Webmaster verificados nos três sites (traz dados reais de busca).
5. Política de privacidade: revisar com contador/advogado antes de publicar a medição, inclusive quem é o responsável pelos dados em cada site.

## 8. Riscos conhecidos
- Fontes oficiais mudam de endereço; o robô registra "fonte indisponível" em vez de inventar.
- Terceiros erram; por isso o estatuto V/R.
- Plataformas de anúncio mudam regras em dias; recomendação antiga pode virar errada (por isso cada regra tem data).
- Sem dados reais de busca e conversão, público-alvo e canal ideal ficam como hipótese (H).
- A tarefa agendada roda numa sessão nova; não está confirmado que ela enxergue o Projeto IA Vendas. Se não enxergar, o robô entrega o resultado por mensagem em vez de gravar no documento.
- O ambiente das sessões do Claude bloqueia downloads externos, criação de tags e de repositórios, e não tem pgvector; testes de integração completos precisam rodar no computador do Carlos.
