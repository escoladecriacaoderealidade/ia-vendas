# IA de Vendas — regras de trabalho (para o Claude e para quem mexer aqui)

Leia este arquivo inteiro antes de qualquer tarefa. Contexto do produto: `README.md` e `docs/arquitetura.md`.

## Quem é o dono
Carlos Farias (José Carlos Rosa Farias), autor e educador de Santa Maria/RS. **Não é programador.** Fale sempre em **português do Brasil**, em linguagem simples, passo a passo. Quando ele precisar clicar em algo (GitHub, Vercel, Railway, Supabase), dê o caminho exato dos menus. Ele costuma mandar fotos da tela. **Nunca peça segredos** (senhas, chaves): ele os digita direto nos cofres.

## Regras que não podem ser quebradas
1. **Confirme antes de ações irreversíveis**: apagar arquivos, forçar push, sobrescrever histórico, mexer em DNS, publicar, **gastar dinheiro** (campanhas, orçamentos). Sem confirmação por escrito, não faça.
2. **Nada é publicado sozinho.** Mudanças em sites e apps vão por **pull request** para o Carlos revisar. Nunca empurre direto na `main` (exceto o primeiro commit deste repositório).
3. **Modos de operação** (do mais seguro ao mais perigoso): (1) recomendar, só leitura; (2) propor mudança por pull request; (3) campanha, só com aprovação e teto de gasto. Nunca aumente orçamento sozinho.
4. **Cada afirmação tem um estatuto**: **V** verificado na fonte oficial (com data) · **R** reportado por terceiros · **I** inferido do código/dados · **H** hipótese · **D** decisão do cliente. Nunca apresente R, I ou H como fato.
5. **Leia as regras do cliente antes de recomendar** (CLAUDE.md, decisões, pendências do repositório dele). Separe **decisão deliberada** de **lacuna**. Exemplo real: o site da Escola não mostra preço de propósito.
6. **Nunca prometa resultado** em textos para clientes ou anúncios (nem cura, nem aprovação, nem "grátis para sempre").
7. **Privacidade (LGPD)**: medição anônima, sem cookies de publicidade, respeitando "Não rastrear". Guarde só o **tipo** de canal; **nunca** códigos de anunciante (gclid, msclkid, fbclid) nem dados pessoais. Mudou o que se coleta? Atualize a política de privacidade do cliente **antes** de publicar.
8. **Antes de criar um evento ou tabela, confira os relatórios existentes**: eles podem contar tudo sem filtro de tipo e ficar distorcidos. Prefira tabela à parte.
9. **Diga o que não foi verificado.** Teste em ambiente real quando possível; se só houve simulação, escreva isso.
10. **Confira números citados** (aconteceu: um pull request disse "21 páginas"; eram 20).

## Ponto de recuperação
Antes de mexer em qualquer repositório de cliente, registre o commit da `main` e crie um branch `backup-AAAA-MM-DD`. O ambiente do Claude **não consegue criar tags nem repositórios** (bloqueio do proxy); `git push` de branches funciona. Gere também um `git archive` para o Carlos guardar. Procedimento completo: documento `guia-de-publicacao-e-recuperacao-2026-11-03` no Projeto IA Vendas.

## Convenções
- Receitas novas seguem o formato de `receitas/README.md`.
- Comentários e mensagens de commit em português.
- Testes sempre que houver código; rode a suíte antes e depois e compare (linha de base).
- Segredos só em variáveis de ambiente / cofres. Modelo de variáveis em `.env.example` (nunca o `.env` real).
