# Como rodar a análise no Windows (passo a passo)

Para quem não programa. O comando só **lê** páginas públicas e grava arquivos na pasta `resultado`. Não altera o site nem o repositório.

## Uma vez só

**1. Ver se o Python está instalado.** No VS Code: menu **Terminal** > **New Terminal**. Digite `python --version` e aperte Enter. Deve aparecer algo como `Python 3.12.1`.
- Se aparecer "não é reconhecido", tente `py --version`.
- Se também não funcionar: abra python.org/downloads, clique no botão amarelo, execute o instalador, **marque a caixa "Add python.exe to PATH"** e clique em **Install Now**. Feche o terminal do VS Code e abra outro.
- Não precisa instalar mais nada (o `pip` não é usado).

**2. Baixar o projeto.** No mesmo terminal, uma linha de cada vez:
```
cd C:\Users\Cliente\Documents\GitHub
git clone https://github.com/escoladecriacaoderealidade/ia-vendas
cd ia-vendas
```
Se o GitHub pedir login, uma janela do navegador abre: entre com a sua conta.

**3. Pegar o código da Fase 1.** Enquanto o pull request #1 não for aceito:
```
git checkout fase-1-coletor
```
Depois que você aceitar o pull request no GitHub (**Merge pull request** > **Confirm merge**), basta `git pull` e este passo não é mais necessário.

## Rodar

**4.** Dentro da pasta `ia-vendas`:
```
python -m ia_vendas analisar --url https://escoladecriacaoderealidade.com.br --saida resultado
```
Leva de 30 segundos a 1 minuto (espera 1 segundo entre as páginas de propósito, por educação com o site). Termina com duas linhas: `Páginas lidas: ...` e `Gravado em: ...`.

**5. Ver o resultado.** No VS Code, barra da esquerda (**Ctrl+Shift+E**) > pasta `resultado` > `relatorio.md`. Para ver bonito: com o arquivo aberto, aperte **Ctrl+Shift+V**.

**6. Me mandar.** Abra o `relatorio.md`, **Ctrl+A**, **Ctrl+C** e cole na conversa. Ou anexe o arquivo.

## Outros usos
- Outro site: troque o endereço depois de `--url`.
- Incluir as regras do projeto do cliente: acrescente `--repo CAMINHO-DA-PASTA-DO-PROJETO` (a pasta do projeto no seu computador).
- Poucas páginas, para testar rápido: acrescente `--max-paginas 10`.

## Se der erro
| O que aparece | O que fazer |
|---|---|
| `python` não é reconhecido | Use `py -m ia_vendas analisar ...` ou reinstale o Python marcando "Add python.exe to PATH" |
| `No module named ia_vendas` | Você não está na pasta `ia-vendas` (`cd C:\Users\Cliente\Documents\GitHub\ia-vendas`) ou esqueceu o passo 3 |
| `Páginas lidas: 0` | Abra o `relatorio.md`: o achado "Nenhuma página pôde ser lida" mostra o motivo. Se citar **SSLCertVerificationError** (certificado), é o mesmo tipo de problema do `pip` neste computador: me mande a mensagem |
| Antivírus ou firewall pergunta algo | Permita o Python acessar a internet |
| Parece travado | **Ctrl+C** para parar e tente com `--max-paginas 10` |
