# Cliente para APIs de COVID-19

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from src.utils.constants import BRASIL_IO_API_URL, WORLD_COVID_API_URL
import time

# Carregar variáveis de ambiente
load_dotenv()

class COVID19APIClient:
    """Cliente para acessar APIs de dados da COVID-19"""
    
    def __init__(self): 
        self.brasil_io_api_key = os.getenv('BRASIL_IO_API_KEY')
        self.brasil_populacao = 215313498  # População do Brasil com base na estimativa do IBGE em 2022
        self.timeout = 10  # Timeout de 10 segundos
        self.max_retries = 2  # Máximo de 2 tentativas
        
    def _make_request(self, url, headers=None, params=None):
        """Faz uma requisição HTTP com retry e timeout"""
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=headers, 
                    params=params, 
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limit
                    time.sleep(2 ** attempt)  # Backoff exponencial
                    continue
                else:
                    print(f"Erro HTTP {response.status_code} na tentativa {attempt + 1}")
                    
            except requests.exceptions.Timeout:
                print(f"Timeout na tentativa {attempt + 1} para {url}")
            except requests.exceptions.ConnectionError:
                print(f"Erro de conexão na tentativa {attempt + 1} para {url}")
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição na tentativa {attempt + 1}: {e}")
                
            if attempt < self.max_retries - 1:
                time.sleep(1)  # Aguarda 1 segundo antes de tentar novamente
                
        return None
        
    def get_brasil_data(self):
        """Obtém dados atuais do Brasil por estado"""
        try:
            url = f"{BRASIL_IO_API_URL}/caso_full/data"
            headers = {
                'Authorization': f'Token {self.brasil_io_api_key}',
                'Content-Type': 'application/json'
            } if self.brasil_io_api_key else {}
            
            params = {
                'place_type': 'state', # Filtrar apenas dados de estados
                'is_last': 'True' # Traz apenas os registros mais recentes
            }
            
            response = self._make_request(url, headers=headers, params=params)
            
            if response and response.status_code == 200:
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
            
            response = self._make_request(url, params=params)
            
            if response and response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    # Filtrar Brasil e pegar apenas os top países
                    df_filtered = df[df['country'] != 'Brazil'].head(limit)
                    return df_filtered
                    
            return None
            
        except Exception as e:
            print(f"Erro ao obter dados mundiais: {e}")
            return None
    
    def get_world_countries_data(self, countries):
        """Obtém dados de países específicos"""
        try:
            if not countries:
                return None
                
            countries_str = ','.join(countries)
            url = f"{WORLD_COVID_API_URL}/countries/{countries_str}"
            
            response = self._make_request(url)
            
            if response and response.status_code == 200:
                data = response.json()
                if data:
                    # Se for um único país, transformar em lista
                    if isinstance(data, dict):
                        data = [data]
                    df = pd.DataFrame(data)
                    return df
                    
            return None
            
        except Exception as e:
            print(f"Erro ao obter dados de países específicos: {e}")
            return None
    
    def get_brasil_historical_data(self, limit=None):
        """Obtém dados históricos do Brasil"""
        try:
            headers = {
                'Authorization': f'Token {self.brasil_io_api_key}',
                'Content-Type': 'application/json'
            } if self.brasil_io_api_key else {}
            
            params = {
                'place_type': 'state'
            }
            if limit:
                params['limit'] = limit
                
            url = f"{BRASIL_IO_API_URL}/caso_full/data"
            response = self._make_request(url, headers=headers, params=params)
            
            if response and response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    df = pd.DataFrame(data['results'])
                    return df
                    
            return None
            
        except Exception as e:
            print(f"Erro ao obter dados históricos do Brasil: {e}")
            return None
    
    def get_brasil_time_series(self, state=None, days=30):
        """Obtém série temporal do Brasil ou de um estado específico"""
        try:
            headers = {
                'Authorization': f'Token {self.brasil_io_api_key}',
                'Content-Type': 'application/json'
            } if self.brasil_io_api_key else {}
            
            params = {
                'place_type': 'state' if state else 'state'
            }
            if state:
                params['state'] = state
                
            url = f"{BRASIL_IO_API_URL}/caso_full/data"
            response = self._make_request(url, headers=headers, params=params)
            
            if response and response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    df = pd.DataFrame(data['results'])
                    # Ordenar por data e pegar os últimos N dias
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'])
                        df = df.sort_values('date').tail(days * len(df['state'].unique()) if not state else days)
                    return df
                    
            return None
            
        except Exception as e:
            print(f"Erro ao obter série temporal: {e}")
            return None
    
    def calculate_moving_averages(self, df, window=7):
        """Calcula médias móveis para os dados"""
        try:
            if df is None or df.empty:
                return df
                
            # Calcular médias móveis para casos e óbitos
            if 'new_confirmed' in df.columns:
                df['ma_cases'] = df['new_confirmed'].rolling(window=window, min_periods=1).mean()
            if 'new_deaths' in df.columns:
                df['ma_deaths'] = df['new_deaths'].rolling(window=window, min_periods=1).mean()
                
            return df
            
        except Exception as e:
            print(f"Erro ao calcular médias móveis: {e}")
            return df