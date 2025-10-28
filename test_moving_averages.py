#!/usr/bin/env python3
"""
Script de teste para verificar se há problemas com médias móveis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.api_client import COVID19APIClient

def test_moving_averages():
    """Testa a função de médias móveis"""
    print("🧪 Testando função de médias móveis...")
    
    # Inicializar cliente
    client = COVID19APIClient()
    
    # Obter dados de série temporal
    print("📊 Obtendo dados de série temporal...")
    time_series_data = client.get_brasil_time_series(days=30)
    
    if time_series_data is None or time_series_data.empty:
        print("❌ Erro: Dados de série temporal não disponíveis")
        return
    
    print(f"✅ Dados obtidos: {len(time_series_data)} registros")
    print(f"📋 Colunas disponíveis: {list(time_series_data.columns)}")
    
    # Calcular médias móveis
    print("📈 Calculando médias móveis...")
    moving_averages = client.calculate_moving_averages(time_series_data)
    
    if moving_averages is None or moving_averages.empty:
        print("❌ Erro: Médias móveis não calculadas")
        return
    
    print(f"✅ Médias móveis calculadas")
    print(f"📋 Colunas após cálculo: {list(moving_averages.columns)}")
    
    # Verificar se as colunas corretas existem
    expected_columns = ['ma_cases', 'ma_deaths']
    missing_columns = [col for col in expected_columns if col not in moving_averages.columns]
    
    if missing_columns:
        print(f"❌ Colunas faltando: {missing_columns}")
    else:
        print("✅ Todas as colunas de médias móveis estão presentes")
    
    # Verificar se há colunas com nomes antigos
    old_columns = ['casos_ma7', 'obitos_ma7']
    found_old_columns = [col for col in old_columns if col in moving_averages.columns]
    
    if found_old_columns:
        print(f"⚠️ Colunas antigas encontradas: {found_old_columns}")
    else:
        print("✅ Nenhuma coluna antiga encontrada")
    
    # Mostrar amostra dos dados
    print("\n📊 Amostra dos dados:")
    print(moving_averages[['state', 'date', 'new_confirmed', 'new_deaths', 'ma_cases', 'ma_deaths']].head())

if __name__ == "__main__":
    test_moving_averages()