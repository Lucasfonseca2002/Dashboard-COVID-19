# Testes unitários para src/utils/helpers.py

import pytest

from src.utils.helpers import format_number, create_metric_card


# ---------------------------------------------------------------------------
# format_number()
# ---------------------------------------------------------------------------

class TestFormatNumber:

    def test_numero_inteiro_grande(self):
        assert format_number(1_000_000) == "1,000,000"

    def test_numero_com_separador_de_milhar(self):
        assert format_number(38_500_000) == "38,500,000"

    def test_zero(self):
        assert format_number(0) == "0"

    def test_numero_pequeno(self):
        assert format_number(42) == "42"

    def test_float_sem_casas_decimais(self):
        assert format_number(1234.9) == "1,235"

    def test_float_com_duas_casas_decimais(self):
        assert format_number(1234.5678, decimal_places=2) == "1,234.57"

    def test_float_com_uma_casa_decimal(self):
        assert format_number(9876.1, decimal_places=1) == "9,876.1"

    def test_none_retorna_na(self):
        assert format_number(None) == "N/A"

    def test_valor_invalido_retorna_na(self):
        assert format_number("texto_invalido") == "N/A"

    def test_negativo(self):
        assert format_number(-5_000) == "-5,000"


# ---------------------------------------------------------------------------
# create_metric_card()
# ---------------------------------------------------------------------------

class TestCreateMetricCard:

    def test_retorna_dict(self):
        result = create_metric_card("Casos", 1_000_000)
        assert isinstance(result, dict)

    def test_chaves_presentes(self):
        result = create_metric_card("Casos", 1_000_000)
        assert set(result.keys()) == {"title", "value", "description", "delta", "delta_color"}

    def test_title_correto(self):
        result = create_metric_card("Total de Casos", 5_000)
        assert result["title"] == "Total de Casos"

    def test_value_correto(self):
        result = create_metric_card("Óbitos", 170_000)
        assert result["value"] == 170_000

    def test_description_padrao_vazia(self):
        result = create_metric_card("Casos", 0)
        assert result["description"] == ""

    def test_delta_padrao_none(self):
        result = create_metric_card("Casos", 0)
        assert result["delta"] is None

    def test_delta_color_padrao(self):
        result = create_metric_card("Casos", 0)
        assert result["delta_color"] == "normal"

    def test_parametros_opcionais(self):
        result = create_metric_card(
            title="Novos Casos",
            value=500,
            description="Casos nas últimas 24h",
            delta="+50",
            delta_color="inverse",
        )
        assert result["description"] == "Casos nas últimas 24h"
        assert result["delta"] == "+50"
        assert result["delta_color"] == "inverse"

    def test_value_pode_ser_string(self):
        result = create_metric_card("Taxa", "2.5%")
        assert result["value"] == "2.5%"

    def test_value_pode_ser_zero(self):
        result = create_metric_card("Sem dados", 0)
        assert result["value"] == 0
