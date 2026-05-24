# Testes unitários para src/data/data_processor.py

import pytest
import pandas as pd

from src.data.data_processor import calculate_totals, calculate_mortality_rate, get_top_states


@pytest.fixture
def df_estados():
    """DataFrame com dados fictícios de estados brasileiros."""
    return pd.DataFrame([
        {
            "state": "SP",
            "last_available_confirmed": 5_000_000,
            "last_available_deaths": 170_000,
            "new_confirmed": 500,
            "new_deaths": 10,
        },
        {
            "state": "RJ",
            "last_available_confirmed": 2_000_000,
            "last_available_deaths": 80_000,
            "new_confirmed": 200,
            "new_deaths": 4,
        },
        {
            "state": "MG",
            "last_available_confirmed": 3_000_000,
            "last_available_deaths": 90_000,
            "new_confirmed": 300,
            "new_deaths": 6,
        },
    ])


# ---------------------------------------------------------------------------
# calculate_totals()
# ---------------------------------------------------------------------------

class TestCalculateTotals:

    def test_soma_correta_de_casos(self, df_estados):
        result = calculate_totals(df_estados)
        assert result["total_cases"] == 10_000_000

    def test_soma_correta_de_obitos(self, df_estados):
        result = calculate_totals(df_estados)
        assert result["total_deaths"] == 340_000

    def test_soma_correta_de_novos_casos(self, df_estados):
        result = calculate_totals(df_estados)
        assert result["new_cases"] == 1_000

    def test_soma_correta_de_novos_obitos(self, df_estados):
        result = calculate_totals(df_estados)
        assert result["new_deaths"] == 20

    def test_retorna_zeros_para_dataframe_vazio(self):
        result = calculate_totals(pd.DataFrame())
        assert result == {"total_cases": 0, "total_deaths": 0, "new_cases": 0, "new_deaths": 0}

    def test_retorna_zeros_para_none(self):
        result = calculate_totals(None)
        assert result == {"total_cases": 0, "total_deaths": 0, "new_cases": 0, "new_deaths": 0}

    def test_retorna_zeros_quando_colunas_ausentes(self):
        df = pd.DataFrame([{"state": "SP"}])
        result = calculate_totals(df)
        assert result["total_cases"] == 0
        assert result["total_deaths"] == 0

    def test_retorna_dict(self, df_estados):
        result = calculate_totals(df_estados)
        assert isinstance(result, dict)
        assert set(result.keys()) == {"total_cases", "total_deaths", "new_cases", "new_deaths"}


# ---------------------------------------------------------------------------
# calculate_mortality_rate()
# ---------------------------------------------------------------------------

class TestCalculateMortalityRate:

    def test_calculo_correto(self):
        rate = calculate_mortality_rate(total_cases=1_000, total_deaths=20)
        assert rate == pytest.approx(2.0)

    def test_retorna_zero_quando_sem_casos(self):
        assert calculate_mortality_rate(0, 0) == 0.0

    def test_retorna_zero_quando_cases_none(self):
        assert calculate_mortality_rate(None, 10) == 0.0

    def test_arredondamento_a_duas_casas(self):
        rate = calculate_mortality_rate(total_cases=3, total_deaths=1)
        assert rate == pytest.approx(33.33)

    def test_taxa_100_por_cento(self):
        assert calculate_mortality_rate(100, 100) == pytest.approx(100.0)

    def test_taxa_menor_que_1_porcento(self):
        rate = calculate_mortality_rate(total_cases=100_000, total_deaths=50)
        assert rate == pytest.approx(0.05)


# ---------------------------------------------------------------------------
# get_top_states()
# ---------------------------------------------------------------------------

class TestGetTopStates:

    def test_retorna_top_n_correto(self, df_estados):
        result = get_top_states(df_estados, "last_available_confirmed", n=2)
        assert len(result) == 2

    def test_ordenado_do_maior_para_menor(self, df_estados):
        result = get_top_states(df_estados, "last_available_confirmed", n=3)
        values = result["last_available_confirmed"].tolist()
        assert values == sorted(values, reverse=True)

    def test_primeiro_estado_e_sp(self, df_estados):
        result = get_top_states(df_estados, "last_available_confirmed", n=1)
        assert result.iloc[0]["state"] == "SP"

    def test_retorna_dataframe_vazio_para_none(self):
        result = get_top_states(None, "last_available_confirmed")
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_retorna_dataframe_vazio_para_df_vazio(self):
        result = get_top_states(pd.DataFrame(), "last_available_confirmed")
        assert result.empty

    def test_retorna_dataframe_vazio_para_coluna_inexistente(self, df_estados):
        result = get_top_states(df_estados, "coluna_inexistente")
        assert result.empty

    def test_n_maior_que_total_de_linhas_retorna_todas(self, df_estados):
        result = get_top_states(df_estados, "last_available_confirmed", n=100)
        assert len(result) == len(df_estados)

    def test_n_padrao_e_5(self, df_estados):
        result = get_top_states(df_estados, "last_available_confirmed")
        assert len(result) <= 5
