import pandas as pd
from typing import List

def get_fallback_brasil_data() -> pd.DataFrame:
    """Retorna dados de fallback para o Brasil quando a API não está disponível"""
    # Dados simulados baseados em dados reais aproximados
    fallback_data = {
        'state': ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'GO', 'PE', 'CE'],
        'last_available_confirmed': [6200000, 2800000, 2400000, 1600000, 1500000, 1400000, 1300000, 900000, 800000, 700000],
        'last_available_deaths': [180000, 85000, 65000, 42000, 45000, 25000, 32000, 28000, 22000, 27000],
        'new_confirmed': [1200, 800, 600, 400, 350, 300, 250, 200, 180, 150],
        'new_deaths': [25, 18, 15, 12, 10, 8, 7, 6, 5, 4],
        'city': [None] * 10,
        'place_type': ['state'] * 10,
        'date': ['2024-01-15'] * 10
    }
    return pd.DataFrame(fallback_data)

def get_fallback_world_data(limit: int = 10) -> pd.DataFrame:
    """Retorna dados de fallback para países quando a API não está disponível"""
    # Dados simulados baseados em dados reais aproximados
    fallback_data = {
        'country': ['USA', 'India', 'France', 'Germany', 'Iran', 'Russia', 'South Korea', 'Japan', 'Italy', 'Turkey'],
        'cases': [103000000, 45000000, 38000000, 38000000, 7500000, 22000000, 31000000, 33000000, 26000000, 17000000],
        'deaths': [1120000, 530000, 174000, 174000, 145000, 400000, 34000, 74000, 190000, 102000],
        'todayCases': [15000, 8000, 12000, 9000, 500, 3000, 2500, 4000, 3500, 2000],
        'todayDeaths': [150, 80, 45, 35, 15, 25, 5, 20, 18, 12],
        'population': [331000000, 1380000000, 65000000, 83000000, 84000000, 146000000, 51000000, 126000000, 60000000, 84000000]
    }
    return pd.DataFrame(fallback_data).head(limit)

def get_fallback_countries_data(countries: List[str]) -> pd.DataFrame:
    """Retorna dados de fallback para países específicos quando a API não está disponível"""
    # Dados simulados para países específicos
    fallback_mapping = {
        'USA': {'country': 'USA', 'cases': 103000000, 'deaths': 1120000, 'population': 331000000},
        'India': {'country': 'India', 'cases': 45000000, 'deaths': 530000, 'population': 1380000000},
        'France': {'country': 'France', 'cases': 38000000, 'deaths': 174000, 'population': 65000000},
        'Germany': {'country': 'Germany', 'cases': 38000000, 'deaths': 174000, 'population': 83000000},
        'Iran': {'country': 'Iran', 'cases': 7500000, 'deaths': 145000, 'population': 84000000},
        'Russia': {'country': 'Russia', 'cases': 22000000, 'deaths': 400000, 'population': 146000000},
        'South Korea': {'country': 'South Korea', 'cases': 31000000, 'deaths': 34000, 'population': 51000000},
        'Japan': {'country': 'Japan', 'cases': 33000000, 'deaths': 74000, 'population': 126000000},
        'Italy': {'country': 'Italy', 'cases': 26000000, 'deaths': 190000, 'population': 60000000},
        'Turkey': {'country': 'Turkey', 'cases': 17000000, 'deaths': 102000, 'population': 84000000}
    }

    fallback_data = []
    for country in countries:
        if country in fallback_mapping:
            fallback_data.append(fallback_mapping[country])

    if fallback_data:
        return pd.DataFrame(fallback_data)
    else:
        return pd.DataFrame()