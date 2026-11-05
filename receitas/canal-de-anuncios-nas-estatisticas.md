# Receita: reconhecer o canal de anúncios pagos na medição própria

**Quando usar:** a medição guarda o canal de origem (utm_source ou site de referência), mas cliques vindos de anúncios aparecem como "direto".

**O que verificar:** a função que calcula o canal; procurar tratamento de `gclid`, `gbraid`, `wbraid`, `msclkid`, `fbclid`.

**Critério de "certo":** ordem de prioridade — `utm_source` > `gclid/gbraid/wbraid` = `google-ads` > `msclkid` = `bing-ads` > `fbclid` = `meta` (o fbclid também vem de posts comuns do Facebook/Instagram, R: relatado por terceiros, sem documentação da Meta; por isso não se chama meta-ads) > site de referência > `direto`. O primeiro toque fica guardado e não é sobrescrito. Testar com casos simulados (cada parâmetro, utm junto com gclid, referência do Google, direto, primeiro toque preservado).

**Como corrigir:** acrescentar as linhas no cálculo do canal, só no lado do cliente, sem mexer em API ou banco.

**Cuidados:** guardar **somente o tipo** de canal; nunca o código do anunciante. Isso não envia conversões às plataformas de anúncio (assunto à parte, exige decisão e consentimento).

**Caso real:** app Enquanto (`canal()` em `src/enquanto.html`).
