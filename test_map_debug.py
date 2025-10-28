#!/usr/bin/env python3
"""
Script para testar e debugar a funcionalidade do mapa interativo
"""

from src.data.api_client import COVID19APIClient
import pandas as pd

def test_map_data():
    """Testa os dados necessários para o mapa"""
    print("=== TESTE DOS DADOS DO MAPA ===")
    
    # Inicializar cliente da API
    api = COVID19APIClient()
    
    # Carregar dados
    print("Carregando dados...")
    data = api.get_brasil_data()
    
    if data is None:
        print("❌ ERRO: Dados não disponíveis")
        return False
        
    print(f"✅ Dados carregados: {len(data)} registros")
    
    # Verificar colunas necessárias
    required_cols = ['state', 'last_available_confirmed', 'last_available_deaths', 'estimated_population']
    missing_cols = [col for col in required_cols if col not in data.columns]
    
    if missing_cols:
        print(f"❌ Colunas faltantes: {missing_cols}")
        return False
    else:
        print("✅ Todas as colunas necessárias estão presentes")
    
    # Verificar estados únicos
    states = data['state'].unique()
    print(f"Estados encontrados: {len(states)}")
    print(f"Lista de estados: {sorted(states)}")
    
    # Verificar valores nulos
    print("\n=== VERIFICAÇÃO DE VALORES NULOS ===")
    for col in required_cols:
        null_count = data[col].isnull().sum()
        print(f"{col}: {null_count} valores nulos")
    
    # Verificar coordenadas dos estados
    state_coords = {
        'AC': [-8.77, -70.55], 'AL': [-9.71, -35.73], 'AP': [1.41, -51.77],
        'AM': [-3.07, -61.66], 'BA': [-12.96, -38.51], 'CE': [-3.71, -38.54],
        'DF': [-15.83, -47.86], 'ES': [-19.19, -40.34], 'GO': [-16.64, -49.31],
        'MA': [-2.55, -44.30], 'MT': [-12.64, -55.42], 'MS': [-20.51, -54.54],
        'MG': [-18.10, -44.38], 'PA': [-5.53, -52.29], 'PB': [-7.06, -35.55],
        'PR': [-24.89, -51.55], 'PE': [-8.28, -35.07], 'PI': [-8.28, -42.83],
        'RJ': [-22.84, -43.15], 'RN': [-5.22, -36.52], 'RO': [-11.22, -62.80],
        'RR': [1.89, -61.22], 'RS': [-30.01, -51.22], 'SC': [-27.33, -49.44],
        'SE': [-10.90, -37.07], 'SP': [-23.55, -46.64], 'TO': [-10.25, -48.25]
    }
    
    states_without_coords = [state for state in states if state not in state_coords]
    if states_without_coords:
        print(f"❌ Estados sem coordenadas: {states_without_coords}")
        return False
    else:
        print("✅ Todos os estados têm coordenadas definidas")
    
    # Testar cálculo de métricas
    print("\n=== TESTE DE CÁLCULO DE MÉTRICAS ===")
    try:
        # Taxa de mortalidade
        data['taxa_mortalidade'] = (data['last_available_deaths'] / data['last_available_confirmed'] * 100).fillna(0)
        print(f"✅ Taxa de mortalidade calculada (min: {data['taxa_mortalidade'].min():.2f}%, max: {data['taxa_mortalidade'].max():.2f}%)")
        
        # Incidência por 100k
        if 'last_available_confirmed_per_100k_inhabitants' in data.columns:
            data['incidencia_100k'] = data['last_available_confirmed_per_100k_inhabitants']
        else:
            data['incidencia_100k'] = (data['last_available_confirmed'] / data['estimated_population'] * 100000)
        print(f"✅ Incidência por 100k calculada (min: {data['incidencia_100k'].min():.2f}, max: {data['incidencia_100k'].max():.2f})")
        
    except Exception as e:
        print(f"❌ Erro no cálculo de métricas: {e}")
        return False
    
    print("\n=== TESTE DE IMPORTAÇÃO DO FOLIUM ===")
    try:
        import folium
        from streamlit_folium import st_folium
        print("✅ Folium e streamlit-folium importados com sucesso")
        
        # Teste básico de criação de mapa
        m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
        print("✅ Mapa base criado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro na importação/criação do mapa: {e}")
        return False
    
    print("\n🎉 TODOS OS TESTES PASSARAM! O mapa deveria funcionar.")
    return True

if __name__ == "__main__":
    test_map_data()