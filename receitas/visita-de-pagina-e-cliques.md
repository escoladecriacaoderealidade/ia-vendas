# Receita: medir visita de página e cliques para o app, sem cookies

**Quando usar:** páginas públicas (guias, vitrine) levam ao app, mas ninguém sabe quais páginas e quais canais trazem gente.

**O que verificar:** (1) se já existe medição de eventos e **como os relatórios contam** (aconteceu: o painel contava aparelhos sem filtro de tipo, então visitas de página inflariam "usuários"); (2) se o site e o app estão na mesma origem (compartilham `localStorage`) ou em origens diferentes.

**Critério de "certo":** tabela **à parte** das existentes; endpoint que valida tudo (origem permitida, código do aparelho, tipo, página, tamanho dos textos), ignora robôs e nunca quebra a página; script que respeita "Não rastrear" (não envia e não cria código); testes do script e do endpoint com simulações.

**Como corrigir:** no mesmo domínio do app, reaproveitar as chaves do app (código do aparelho e canal) para a mesma pessoa aparecer do começo ao fim. Em domínio diferente, **não** ligar a pessoa entre sites: repassar o canal de origem como `utm_source` nos links para o app. Enviar com `sendBeacon` e corpo `text/plain` (evita a checagem prévia CORS).

**Cuidados:** atualizar a política de privacidade **antes** de publicar; confirmar com contador/advogado quem é o responsável pelos dados em cada site; ordem de publicação: banco → API → sites; o endpoint não grava nada enquanto a tabela não existir, então publicar o código antes é seguro.

**Caso real:** Enquanto Estuda (páginas de guia) e site da Escola.
