"""Testes adicionais: desempate do ranking, limites do --top, ordenação por mês e códigos de saída."""

import os
import subprocess
import sys

from helpers import PROJECT_ROOT, SRC_DIR, run_cli


def _executar(argumentos):
    """Roda o CLI sem exigir sucesso, para inspecionar o código de saída."""
    ambiente = os.environ.copy()
    ambiente["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + ambiente.get("PYTHONPATH", "")
    ambiente["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "onfly_report", *argumentos],
        cwd=str(PROJECT_ROOT),
        env=ambiente,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_top_hotels_empate_desempata_por_hotel_id_crescente(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H03", "hotel_name": "C", "amount": "500.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "A", "amount": "500.00"},
            {"reservation_id": "R-3", "hotel_id": "H02", "hotel_name": "B", "amount": "500.00"},
        ],
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01", "H02", "H03"]


def test_top_maior_que_numero_de_hoteis_devolve_so_os_existentes(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "amount": "200.00"},
        ],
        top=10,
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H02", "H01"]


def test_top_um_devolve_apenas_o_primeiro(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "amount": "200.00"},
        ],
        top=1,
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H02"]


def test_by_month_ordenado_por_mes_ascendente_e_usa_mes_do_checkin(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "checkin_date": "2025-03-10", "checkout_date": "2025-03-11"},
            {"reservation_id": "R-2", "checkin_date": "2025-01-31", "checkout_date": "2025-02-02"},
            {"reservation_id": "R-3", "checkin_date": "2024-12-30", "checkout_date": "2025-01-02"},
        ],
    )
    assert [m["month"] for m in report["by_month"]] == ["2024-12", "2025-01", "2025-03"]
    janeiro = report["by_month"][1]
    assert janeiro["room_nights"] == 2


def test_cancelados_e_no_show_contam_mas_nao_entram_em_valores_nem_ranking(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CONFIRMED", "amount": "100.00"},
            {"reservation_id": "R-2", "status": "CANCELLED", "hotel_id": "H02", "amount": "999.00"},
            {"reservation_id": "R-3", "status": "NO_SHOW", "hotel_id": "H03", "amount": "999.00"},
        ],
    )
    resumo = report["summary"]
    assert resumo["total_reservations"] == 3
    assert resumo["confirmed_reservations"] == 1
    assert resumo["cancelled_reservations"] == 1
    assert resumo["no_show_reservations"] == 1
    assert resumo["total_amount_brl"] == "100.00"
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01"]
    assert len(report["by_month"]) == 1


def test_saida_2_quando_arquivo_de_reservas_nao_existe(tmp_path):
    taxas = tmp_path / "rates.csv"
    taxas.write_text("currency,rate_to_brl\nBRL,1.000000\n", encoding="utf-8")
    processo = _executar(
        [
            "--input", str(tmp_path / "nao_existe.csv"),
            "--rates", str(taxas),
            "--output", str(tmp_path / "out.json"),
        ]
    )
    assert processo.returncode == 2


def test_saida_2_quando_faltam_colunas_obrigatorias(tmp_path):
    entrada = tmp_path / "reservas.csv"
    entrada.write_text("reservation_id,status\nR-1,CONFIRMED\n", encoding="utf-8")
    taxas = tmp_path / "rates.csv"
    taxas.write_text("currency,rate_to_brl\nBRL,1.000000\n", encoding="utf-8")
    processo = _executar(
        ["--input", str(entrada), "--rates", str(taxas), "--output", str(tmp_path / "out.json")]
    )
    assert processo.returncode == 2


def test_saida_2_quando_top_menor_que_um(tmp_path):
    entrada = tmp_path / "reservas.csv"
    entrada.write_text("reservation_id\n", encoding="utf-8")
    taxas = tmp_path / "rates.csv"
    taxas.write_text("currency,rate_to_brl\nBRL,1.000000\n", encoding="utf-8")
    processo = _executar(
        ["--input", str(entrada), "--rates", str(taxas), "--top", "0"]
    )
    assert processo.returncode == 2
