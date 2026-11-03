# Receita: tags de compartilhamento (Open Graph e cartão do X/Twitter)

**Quando usar:** ao colar o link do site numa conversa ou rede, a prévia sai sem imagem ou sem título bom.

**O que verificar:** em cada página, procurar `og:image`, `og:site_name`, `twitter:card`, `twitter:title`, `twitter:image` no `<head>`. Conferir se o cliente já não tem gerador de páginas (alterar o gerador, não os arquivos gerados).

**Critério de "certo":** cada tag aparece **uma única vez** por página; os blocos JSON-LD continuam válidos; rodar o gerador duas vezes não muda nada (idempotente).

**Como corrigir:** um script sem dependências percorre os HTML, copia título/descrição das tags `og:` existentes, usa uma imagem padrão quando a página não tem capa própria, e insere as tags que faltam depois da última `og:`. O gerador de páginas chama o script ao final.

**Cuidados:** `twitter:card` = `summary` serve para capas em pé e logotipos quadrados. Uma imagem 1200×630 melhora a prévia; peça ao cliente. Não mexer no visual.

**Caso real:** Escola de Criação de Realidade, 20 páginas (`tools/metadados_sociais.py`).
