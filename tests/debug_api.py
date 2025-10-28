# Debug das APIs

import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.data.api_client import COVID19APIClient
    import pandas as pd
    import requests
    
    print("="*60)
    print("🔍 DIAGNÓSTICO DAS APIs")
    print("="*60)
    
    # Verificar arquivo .env
    print("\n📋 Verificando arquivo .env...")
    if os.path.exists('.env'):
        print("✅ Arquivo .env encontrado")
        with open('.env', 'r') as f:
            content = f.read()
            if 'BRASIL_IO_API_KEY' in content:
                print("✅ Variável BRASIL_IO_API_KEY encontrada")
            else:
                print("❌ Variável BRASIL_IO_API_KEY não encontrada")
    else:
        print("❌ Arquivo .env não encontrado")
    
    # Criar cliente
    print("\n🔧 Criando cliente da API...")
    client = COVID19APIClient()
    print(f"✅ Cliente criado")
    print(f"   • Chave API carregada: {'Sim' if client.brasil_io_api_key else 'Não'}")
    
    # Teste 1: API Mundial (sem autenticação)
    print("\n🌍 TESTE 1: API Mundial...")
    try:
        url = "https://disease.sh/v3/covid-19/countries"
        response = requests.get(url, params={'sort': 'cases'})
        print(f"   • Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   • Países encontrados: {len(data)}")
            if len(data) > 0:
                print(f"   • Primeiro país: {data[0].get('country', 'N/A')}")
                print("✅ API Mundial funcionando!")
            else:
                print("❌ API Mundial retornou dados vazios")
        else:
            print(f"❌ API Mundial falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na API Mundial: {e}")
    
    # Teste 2: API Brasil.io (com autenticação)
    print("\n🇧🇷 TESTE 2: API Brasil.io...")
    try:
        url = "https://api.brasil.io/v1/dataset/covid19/caso_full/data"
        headers = {
            'Authorization': f'Token {client.brasil_io_api_key}',
            'Content-Type': 'application/json'
        }
        params = {
            'place_type': 'state',
            'is_last': 'True'
        }
        
        print(f"   • URL: {url}")
        print(f"   • Headers: {headers}")
        print(f"   • Params: {params}")
        
        response = requests.get(url, headers=headers, params=params)
        print(f"   • Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                print(f"   • Registros encontrados: {len(data['results'])}")
                if len(data['results']) > 0:
                    primeiro = data['results'][0]
                    print(f"   • Primeiro estado: {primeiro.get('state', 'N/A')}")
                    print(f"   • Colunas disponíveis: {list(primeiro.keys())}")
                    print("✅ API Brasil.io funcionando!")
                else:
                    print("❌ API Brasil.io retornou resultados vazios")
            else:
                print("❌ API Brasil.io não retornou 'results'")
        elif response.status_code == 401:
            print("❌ Erro de autenticação - Verifique a chave da API")
        elif response.status_code == 400:
            print("❌ Erro 400 - Parâmetros inválidos")
            print(f"   • Resposta: {response.text[:200]}...")
        else:
            print(f"❌ API Brasil.io falhou: {response.status_code}")
            print(f"   • Resposta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Erro na API Brasil.io: {e}")
    
    # Teste 3: Métodos do cliente
    print("\n🧪 TESTE 3: Métodos do cliente...")
    
    print("   • Testando get_world_top_countries()...")
    df_mundial = client.get_world_top_countries(limit=3)
    if df_mundial is not None and not df_mundial.empty:
        print(f"     ✅ Sucesso! {len(df_mundial)} países encontrados")
        print(f"     • Colunas: {list(df_mundial.columns)}")
    else:
        print("     ❌ Falhou ou retornou vazio")
    
    print("   • Testando get_brasil_data()...")
    df_brasil = client.get_brasil_data()
    if df_brasil is not None and not df_brasil.empty:
        print(f"     ✅ Sucesso! {len(df_brasil)} estados encontrados")
        print(f"     • Colunas: {list(df_brasil.columns)}")
    else:
        print("     ❌ Falhou ou retornou vazio")
    
    print("   • Testando get_brasil_historical_data()...")
    df_historico = client.get_brasil_historical_data()
    if df_historico is not None and not df_historico.empty:
        print(f"     ✅ Sucesso! {len(df_historico)} registros históricos")
        print(f"     • Colunas: {list(df_historico.columns)}")
    else:
        print("     ❌ Falhou ou retornou vazio")
    
    print("\n" + "="*60)
    print("✅ DIAGNÓSTICO CONCLUÍDO")
    print("="*60)
        
except Exception as e:
    print(f"❌ Erro geral no diagnóstico: {e}")
    import traceback
    traceback.print_exc()
