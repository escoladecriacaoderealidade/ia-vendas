# Receita: registrar de onde veio cada cadastro

**Quando usar:** o painel mostra quantos se cadastraram, mas não por qual caminho; impossível saber qual canal gera assinantes.

**O que verificar:** onde o usuário é criado (e-mail/senha, login social); se há campo flexível (ex.: `users.metadata` JSON) que evite migração de banco; testes existentes e linha de base de falhas.

**Critério de "certo":** o canal é aceito como campo **opcional**; gravado só em conta **nova** (login de quem já existe não muda o canal); limpo (minúsculas, tamanho limitado, sem caracteres perigosos); falhar ao gravar **nunca** impede o cadastro; relatório por canal com "quantos já pagaram"; suíte completa igual à linha de base + testes novos passando; verificação de tipos do app limpa.

**Como corrigir:** usar o campo JSON existente (zero risco na ordem de publicação banco → API → site); no app, capturar o canal do **primeiro** acesso e enviá-lo no cadastro; criar rota de relatório para administradores.

**Cuidados:** a API pode ser publicada automaticamente ao aceitar o pull request — avisar. Atualizar a política de privacidade do app com uma frase sobre a origem do cadastro.

**Caso real:** Imitação de Cristo (`auth.save_signup_channel`, `reports.signup_channels`, `src/channel.ts`).
