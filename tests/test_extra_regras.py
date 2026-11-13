"""Testes adicionais: pontos que os testes fornecidos não cobrem."""

from decimal import Decimal

from helpers import run_cli
from onfly_report.services.currency_converter import convert_to_brl
from onfly_report.services.report_builder import format_money
from onfly_report.services.stay_calculator import calculate_room_nights
from datetime import date


def test_noites_virada_de_ano_e_varios_quartos():
    assert calculate_room_nights(date(2024, 12, 30), date(2025, 1, 2), 2) == 6


def test_conversao_usa_multiplicacao_e_decimal_exato():
    resultado = convert_to_brl(Decimal("233.79"), "EUR", {"EUR": Decimal("5.88")})
    assert resultado == Decimal("1374.6852")


def test_arredondamento_half_up_somente_na_saida():
    assert format_money(Decimal("0.005")) == "0.01"
    assert format_money(Decimal("2.675")) == "2.68"
    assert format_money(Decimal("10")) == "10.00"


def test_sem_noites_media_zero(tmp_path):
    report = run_cli(tmp_path, [{"reservation_id": "R-1", "status": "CANCELLED"}])
    assert report["summary"]["total_room_nights"] == 0
    assert report["summary"]["average_nightly_rate_brl"] == "0.00"
    assert report["summary"]["cancelled_reservations"] == 1
    assert report["by_month"] == []
    assert report["top_hotels"] == []


def test_arquivo_com_mais_de_200_reservas_e_lido_por_inteiro(tmp_path):
    linhas = [{"reservation_id": f"R-{i}"} for i in range(250)]
    report = run_cli(tmp_path, linhas)
    assert report["summary"]["total_reservations"] == 250
