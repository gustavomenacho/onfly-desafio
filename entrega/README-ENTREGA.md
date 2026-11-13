# Entrega: Recruta Onfly 2026 (Teste Técnico)

Candidato: Gustavo Menacho de Almeida

> **Uso de IA:** trabalhei neste desafio com o apoio do Claude Code (modelo Claude Sonnet 5.5), que executou a
> investigação e as correções sob a minha revisão. A declaração completa e a sessão exportada estão em
> `entrega/uso-de-ia/`.

## Defeitos corrigidos e causa raiz

| # | Arquivo | Defeito | Causa raiz |
|---|---------|---------|------------|
| 1 | `services/currency_converter.py` | Valores em BRL errados | A conversão **dividia** pela taxa e passava por `float`; o correto é `amount * rate_to_brl`, em `Decimal`. |
| 2 | `services/status_policy.py` | NO_SHOW entrava nos totais | A regra era `status != "CANCELLED"`; só `CONFIRMED` é faturável. |
| 3 | `services/stay_calculator.py` | Noites erradas na virada de mês (resultado negativo) | Subtraía só o dia do mês (`checkout.day - checkin.day`) em vez da diferença de datas (`(checkout - checkin).days`). |
| 4 | `services/report_builder.py` | `top_hotels` em ordem invertida | A ordenação era crescente por valor; o contrato pede decrescente por `total_brl` e, no empate, `hotel_id` crescente. |
| 5 | `repositories/csv_reservation_repository.py` | Só 200 das 300 reservas eram lidas | Havia um `break` ao chegar em 200 linhas, que truncava o arquivo e distorcia todos os totais. |

## Como investiguei

1. Leitura do README e das regras de negócio (status, noites, câmbio, exatidão, ordenação).
2. Execução do `pytest -q`: 5 falhas, uma por defeito de lógica.
3. Cada falha foi seguida até a função responsável e comparada com a regra do README.
4. O defeito 5 não aparece em nenhum teste fornecido. Foi achado comparando o número de linhas do CSV (300) com o
   `total_reservations` gerado (200).
5. Validação com a amostra `data/exemplo-validacao.csv`, comparada com a tabela do README.
6. Conferência dos dados reais (status, moedas, quartos, datas, ids) para ver se havia outros casos não cobertos.

## Como validar

```bash
python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

Amostra de validação (`data/exemplo-validacao.csv`): 12 reservas, 9 confirmadas, 2 canceladas, 1 no-show,
28 noites, R$ 7.566,00 e média R$ 270,21, idêntico ao README. Meses: 2025-01 (8 / 25 / 6684.00) e
2025-02 (1 / 3 / 882.00). Top 5: H01, H02, H12, H10, H09.

Dados reais: 300 reservas, 235 confirmadas, 1.347 noites, R$ 396.170,00.

## Resultado do pytest

```
18 passed
```

- 5 testes fornecidos, sem alteração.
- 5 testes novos em `tests/test_extra_regras.py`: noites na virada de ano com vários quartos, conversão exata em
  `Decimal`, arredondamento half-up, relatório sem noites (média `"0.00"`) e arquivo com mais de 200 reservas.
- 8 testes novos em `tests/test_extra_cli.py`: desempate do `top_hotels` por `hotel_id`, `--top` maior que o número
  de hotéis e igual a 1, `by_month` em ordem ascendente pelo mês do check-in, cancelados e no-show contados mas fora
  de valores e ranking, e código de saída 2 para arquivo ausente, colunas faltando e `--top 0`.

Observação: rodei com Python 3.12 (o 3.11 não estava instalado na minha máquina). O código usa só recursos do 3.11.
