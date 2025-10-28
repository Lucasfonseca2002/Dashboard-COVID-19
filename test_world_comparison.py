#!/usr/bin/env python3
"""
Script de teste para verificar dados da comparação mundial
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.api_client import COVID19APIClient

def test_world_comparison():
    """Testa a função de comparação mundial"""
    print("🧪 Testando função de comparação mundial...")
    
    # Inicializar cliente
    client = COVID19APIClient()
    
    # Países de teste
    countries = ['USA', 'India', 'France', 'Germany', 'South Korea']
    print(f"🌍 Testando países: {', '.join(countries)}")
    
    # Obter dados dos países
    print("📊 Obtendo dados dos países...")
    try:
        world_data = client.get_world_countries_data(countries)
        
        if world_data is None or world_data.empty:
            print("❌ Erro: Dados mundiais não disponíveis")
            print("🔄 Tentando método alternativo...")
            
            # Tentar método alternativo
            world_data = client.get_world_top_countries(limit=10)
            if world_data is not None and not world_data.empty:
                print(f"✅ Dados alternativos obtidos: {len(world_data)} países")
                print(f"📋 Colunas disponíveis: {list(world_data.columns)}")
                print("\n📊 Amostra dos dados:")
                print(world_data.head())
            else:
                print("❌ Nenhum método funcionou")
                return
        else:
            print(f"✅ Dados obtidos: {len(world_data)} países")
            print(f"📋 Colunas disponíveis: {list(world_data.columns)}")
            print("\n📊 Amostra dos dados:")
            print(world_data.head())
        
        # Verificar se as colunas necessárias existem
        required_columns = ['country', 'cases', 'deaths']
        missing_columns = [col for col in required_columns if col not in world_data.columns]
        
        if missing_columns:
            print(f"⚠️ Colunas faltando: {missing_columns}")
            print("📋 Mapeamento de colunas possível:")
            for col in world_data.columns:
                if 'case' in col.lower() or 'confirm' in col.lower():
                    print(f"   • {col} -> pode ser 'cases'")
                elif 'death' in col.lower() or 'obito' in col.lower():
                    print(f"   • {col} -> pode ser 'deaths'")
                elif 'country' in col.lower() or 'pais' in col.lower():
                    print(f"   • {col} -> pode ser 'country'")
        else:
            print("✅ Todas as colunas necessárias estão presentes")
            
    except Exception as e:
        print(f"❌ Erro ao obter dados: {e}")

if __name__ == "__main__":
    test_world_comparison()