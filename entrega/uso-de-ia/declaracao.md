# Declaração de uso de IA

Usei o Claude Code como assistente de desenvolvimento neste desafio.

**Ferramenta:** Claude Code (aplicativo desktop da Anthropic).
**Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`).

## O que o assistente fez

- Leu o código-fonte, os dados e o README do desafio.
- Montou o ambiente (venv Python 3.12) e rodou o `pytest`.
- Identificou os 5 defeitos e escreveu as correções (conversão de câmbio, política de status, cálculo de noites,
  ordenação do ranking e limite de 200 linhas na leitura do CSV).
- Escreveu os testes adicionais (`tests/test_extra_regras.py` e `tests/test_extra_cli.py`).
- Redigiu o rascunho do `README-ENTREGA.md` e desta declaração.
- Conferiu a entrega contra a cópia original do desafio, por hash: só os 5 arquivos de código com defeito mudaram;
  os testes fornecidos e os CSVs de dados ficaram idênticos.
- Fez o `git init`, o commit e, a meu pedido, criou o repositório público na minha conta do GitHub.

## O que eu fiz

- Escolhi usar IA neste desafio, baixei o material do Drive e acompanhei o trabalho.
- Revisei as correções e os testes.
- Os comandos (`pytest`, CLI, git) rodaram na minha máquina, pela sessão do Claude Code, e eu acompanhei os resultados.
- Defini o que entrava na entrega: autorizei a publicação, o nome e o e-mail usados nos commits e a redação de dados
  pessoais da sessão exportada.
- Preenchi e enviei o formulário de entrega.

## Resumo da sessão

1. O assistente leu o enunciado e rodou o `pytest`: os 5 testes de lógica falhavam, um por defeito.
2. Seguiu cada falha até a função responsável e comparou com a regra do README (status, noites, câmbio, ordenação).
3. Achou o 5º defeito, que nenhum teste fornecido cobre, comparando as 300 linhas do CSV com os 200
   `total_reservations` que o CLI gerava (havia um `break` aos 200 registros).
4. Validou com a amostra `data/exemplo-validacao.csv` (12 reservas, 28 noites, R$ 7.566,00), que bateu com o README.
5. Escreveu testes extras para as regras que os testes fornecidos não exercitam e documentou tudo no `README-ENTREGA.md`.
6. Numa sessão final de conferência, reexecutou os testes (18 passando), o CLI na amostra e nos dados reais
   (300 reservas, 235 confirmadas, 1.347 noites, R$ 396.170,00) e comparou o projeto com o original.

## Sessão exportada

A sessão do Claude Code está em `entrega/uso-de-ia/sessao-01.jsonl`, exportada pelo recurso de exportação do aplicativo
(o `/export` não estava disponível nessa sessão). O arquivo é o transcript original, com uma única alteração: o e-mail
da conta foi trocado por `[e-mail removido]` e o nome de usuário do Windows nos caminhos de arquivo foi trocado por
`<usuario>`, para não publicar dados pessoais. O restante não foi editado.
