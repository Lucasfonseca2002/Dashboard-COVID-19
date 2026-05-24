# Testes unitários para COVID19APIClient

import pytest
import pandas as pd
from unittest.mock import MagicMock

from src.data.api_client import COVID19APIClient

@pytest.fixture
def client():
    """Instância limpa do cliente para cada teste."""
    return COVID19APIClient()


def _mock_response(json_data, status_code=200):
    """Cria um mock de requests.Response com os dados fornecidos."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    return mock


# ---------------------------------------------------------------------------
# get_brasil_data()
# ---------------------------------------------------------------------------

class TestGetBrasilData:

    SAMPLE_RESULTS = [
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
    ]

    def test_retorna_dataframe_em_sucesso(self, client, mocker):
        """Deve retornar um DataFrame com as linhas da resposta JSON."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response({"results": self.SAMPLE_RESULTS}),
        )

        df = client.get_brasil_data()

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "state" in df.columns

    def test_colunas_presentes(self, client, mocker):
        """O DataFrame deve conter as colunas esperadas."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response({"results": self.SAMPLE_RESULTS}),
        )

        df = client.get_brasil_data()

        for col in ("last_available_confirmed", "last_available_deaths", "new_confirmed", "new_deaths"):
            assert col in df.columns

    def test_retorna_none_quando_results_vazio(self, client, mocker):
        """Deve retornar None quando 'results' estiver presente mas vazio."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response({"results": []}),
        )

        assert client.get_brasil_data() is None

    def test_retorna_none_em_erro_http(self, client, mocker):
        """Deve retornar None quando a resposta HTTP indicar erro."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response({}, status_code=500),
        )

        assert client.get_brasil_data() is None

    def test_retorna_none_quando_make_request_falha(self, client, mocker):
        """Deve retornar None quando _make_request retornar None (sem resposta)."""
        mocker.patch.object(client, "_make_request", return_value=None)

        assert client.get_brasil_data() is None

    def test_retorna_none_quando_chave_results_ausente(self, client, mocker):
        """Deve retornar None quando o JSON não contiver a chave 'results'."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response({"data": []}),
        )

        assert client.get_brasil_data() is None

    def test_usa_filtro_de_estados_nos_params(self, client, mocker):
        """A requisição deve incluir place_type=state e is_last=True."""
        mock_req = mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response({"results": self.SAMPLE_RESULTS}),
        )

        client.get_brasil_data()

        _, kwargs = mock_req.call_args
        params = kwargs.get("params", {})
        assert params.get("place_type") == "state"
        assert params.get("is_last") == "True"


# ---------------------------------------------------------------------------
# get_world_top_countries()
# ---------------------------------------------------------------------------

class TestGetWorldTopCountries:

    SAMPLE_COUNTRIES = [
        {"country": "USA", "cases": 100_000_000, "deaths": 1_000_000},
        {"country": "India", "cases": 45_000_000, "deaths": 500_000},
        {"country": "Brazil", "cases": 38_000_000, "deaths": 700_000},
        {"country": "France", "cases": 35_000_000, "deaths": 160_000},
        {"country": "Germany", "cases": 30_000_000, "deaths": 170_000},
    ]

    def test_retorna_dataframe_em_sucesso(self, client, mocker):
        """Deve retornar um DataFrame quando a API responde com sucesso."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response(self.SAMPLE_COUNTRIES),
        )

        df = client.get_world_top_countries()

        assert df is not None
        assert isinstance(df, pd.DataFrame)

    def test_filtra_brasil(self, client, mocker):
        """Brazil não deve aparecer no resultado."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response(self.SAMPLE_COUNTRIES),
        )

        df = client.get_world_top_countries()

        assert "Brazil" not in df["country"].values

    def test_respeita_parametro_limit(self, client, mocker):
        """Deve retornar no máximo `limit` países."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response(self.SAMPLE_COUNTRIES),
        )

        df = client.get_world_top_countries(limit=2)

        assert len(df) <= 2

    def test_limit_padrao_e_10(self, client, mocker):
        """O limite padrão deve ser 10."""
        countries = [{"country": f"Country{i}", "cases": i * 1000} for i in range(20)]
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response(countries),
        )

        df = client.get_world_top_countries()

        assert len(df) <= 10

    def test_retorna_none_quando_make_request_falha(self, client, mocker):
        """Deve retornar None quando _make_request retornar None."""
        mocker.patch.object(client, "_make_request", return_value=None)

        assert client.get_world_top_countries() is None

    def test_retorna_none_em_resposta_vazia(self, client, mocker):
        """Deve retornar None quando a API retornar lista vazia."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response([]),
        )

        assert client.get_world_top_countries() is None

    def test_retorna_none_em_erro_http(self, client, mocker):
        """Deve retornar None quando o status HTTP indicar erro."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response([], status_code=503),
        )

        assert client.get_world_top_countries() is None

    def test_colunas_presentes(self, client, mocker):
        """O DataFrame deve conter as colunas 'country' e 'cases'."""
        mocker.patch.object(
            client,
            "_make_request",
            return_value=_mock_response(self.SAMPLE_COUNTRIES),
        )

        df = client.get_world_top_countries()

        assert "country" in df.columns
        assert "cases" in df.columns
