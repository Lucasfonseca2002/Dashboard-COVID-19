# Funções de processamento e transformação de dados

import pandas as pd


def calculate_totals(df):
    """Calcula os totais de casos e óbitos a partir de um DataFrame de estados.

    Parâmetros:
    -----------
    df : pandas.DataFrame | None
        DataFrame com colunas 'last_available_confirmed', 'last_available_deaths',
        'new_confirmed' e 'new_deaths'.

    Retorna:
    --------
    dict
        Dicionário com as chaves: total_cases, total_deaths, new_cases, new_deaths.
        Todos os valores são 0 quando o DataFrame está vazio ou é None.
    """
    empty = {"total_cases": 0, "total_deaths": 0, "new_cases": 0, "new_deaths": 0}

    if df is None or df.empty:
        return empty

    return {
        "total_cases": int(df["last_available_confirmed"].sum()) if "last_available_confirmed" in df.columns else 0,
        "total_deaths": int(df["last_available_deaths"].sum()) if "last_available_deaths" in df.columns else 0,
        "new_cases": int(df["new_confirmed"].sum()) if "new_confirmed" in df.columns else 0,
        "new_deaths": int(df["new_deaths"].sum()) if "new_deaths" in df.columns else 0,
    }


def calculate_mortality_rate(total_cases, total_deaths):
    """Calcula a taxa de mortalidade percentual.

    Parâmetros:
    -----------
    total_cases : int | float
        Total de casos confirmados.
    total_deaths : int | float
        Total de óbitos.

    Retorna:
    --------
    float
        Taxa de mortalidade em porcentagem. Retorna 0.0 se total_cases for 0.
    """
    if not total_cases:
        return 0.0
    return round((total_deaths / total_cases) * 100, 2)


def get_top_states(df, column, n=5):
    """Retorna os N estados com maiores valores em uma coluna específica.

    Parâmetros:
    -----------
    df : pandas.DataFrame
        DataFrame com os dados dos estados.
    column : str
        Nome da coluna usada para ordenação.
    n : int
        Quantidade de estados a retornar (padrão 5).

    Retorna:
    --------
    pandas.DataFrame
        Sub-DataFrame ordenado de forma decrescente, com no máximo n linhas.
        Retorna DataFrame vazio se a coluna não existir ou df for None/vazio.
    """
    if df is None or df.empty or column not in df.columns:
        return pd.DataFrame()

    return df.nlargest(n, column).reset_index(drop=True)
