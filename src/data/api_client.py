# Cliente para APIs de COVID-19

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from src.utils.constants import BRASIL_IO_API_URL, WORLD_COVID_API_URL

# Carregar variáveis de ambiente
load_dotenv()

class COVID19APIClient:
    """Cliente para acessar APIs de dados da COVID-19"""
    
    def __init__(self): 
        self.brasil_io_api_key = os.getenv('BRASIL_IO_API_KEY')
        self.brasil_populacao = 215313498  # População do Brasil com base na estimativa do IBGE em 2022
        
    def get_brasil_data(self):
        """Obtém dados atuais do Brasil por estado"""
        try:
            url = f"{BRASIL_IO_API_URL}/caso_full/data"
            headers = {
                'Authorization': f'Token {self.brasil_io_api_key}',
                'Content-Type': 'application/json'
            }
            params = {
                'place_type': 'state', # Filtrar apenas dados de estados
                'is_last': 'True' # Traz apenas os registros mais recentes
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    df = pd.DataFrame(data['results']) # Retorna um dataframe do Pandas com os dados gerados
                    return df
                    
            return None
            
        except Exception as e:
            print(f"Erro ao obter dados do Brasil: {e}")
            return None
    
    def get_world_top_countries(self, limit=10):
        """Obtém dados dos países com mais casos (excluindo Brasil)"""
        try:
            url = f"{WORLD_COVID_API_URL}/countries"
            params = {'sort': 'cases'} # Ordenar por casos confirmados
            
            response = requests.get(url, params=params) 
            
            if response.status_code == 200:
                data = response.json()
                # Filtrar Brasil e pegar apenas os top países
                filtered_data = [country for country in data if country.get('country') != 'Brazil']
                df = pd.DataFrame(filtered_data[:limit])
                return df
                
            return None
            
        except Exception as e:
            print(f"Erro ao obter dados mundiais: {e}")
            return None
    
    def get_world_countries_data(self, countries):
        """Obtém dados específicos de países selecionados"""
        try:
            url = f"{WORLD_COVID_API_URL}/countries"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Filtrar apenas os países solicitados
                filtered_data = [country for country in data if country.get('country') in countries]
                df = pd.DataFrame(filtered_data)
                return df
                
            return None
            
        except Exception as e:
            print(f"Erro ao obter dados de países específicos: {e}")
            return None
    
    def get_brasil_historical_data(self, limit=None):
        """Obtém dados históricos do Brasil com opção de limite"""
        try:
            url = f"{BRASIL_IO_API_URL}/caso_full/data"
            headers = {
                'Authorization': f'Token {self.brasil_io_api_key}',
                'Content-Type': 'application/json'
            }
            params = {
                'place_type': 'state',
                'is_last': 'False'
            }
            
            if limit:
                params['limit'] = limit
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    df = pd.DataFrame(data['results'])
                    # Converter data para datetime
                    df['date'] = pd.to_datetime(df['date'])
                    # Ordenar por data
                    df = df.sort_values(['state', 'date'])
                    return df
                    
            return None
            
        except Exception as e:
            print(f"Erro ao obter dados históricos: {e}")
            return None
    
    def get_brasil_time_series(self, state=None, days=30):
        """Obtém série temporal específica para análise"""
        try:
            df = self.get_brasil_historical_data(limit=2000)
            if df is None:
                return None
            
            # Filtrar por estado se especificado
            if state:
                df = df[df['state'] == state]
            
            # Pegar os últimos N dias
            df = df.tail(days * 27)  # 27 estados * dias
            
            return df
            
        except Exception as e:
            print(f"Erro ao obter série temporal: {e}")
            return None
    
    def calculate_moving_averages(self, df, window=7):
        """Calcula médias móveis para os dados"""
        try:
            if df is None or df.empty:
                return df
            
            df = df.copy()
            df = df.sort_values(['state', 'date'])
            
            # Calcular médias móveis por estado
            for state in df['state'].unique():
                mask = df['state'] == state
                df.loc[mask, 'casos_ma7'] = df.loc[mask, 'new_confirmed'].rolling(window=window, min_periods=1).mean()
                df.loc[mask, 'obitos_ma7'] = df.loc[mask, 'new_deaths'].rolling(window=window, min_periods=1).mean()
            
            return df
            
        except Exception as e:
            print(f"Erro ao calcular médias móveis: {e}")
            return df