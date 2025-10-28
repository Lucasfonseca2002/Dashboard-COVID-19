# Teste dos dados do dashboard

import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.data.api_client import COVID19APIClient
    import pandas as pd
    
    print("="*60)
    print("🔍 TESTE DOS DADOS DO DASHBOARD")
    print("="*60)
    
    # Criar cliente
    client = COVID19APIClient()
    
    # Testar dados por estado
    print("\n📊 Testando dados por estado...")
    df_estados = client.get_brasil_data()
    
    if df_estados is not None and not df_estados.empty:
        print(f"✅ Dados carregados: {len(df_estados)} estados")
        print(f"   • Colunas: {list(df_estados.columns)}")
        
        # Calcular métricas
        total_casos = df_estados['last_available_confirmed'].sum() if 'last_available_confirmed' in df_estados.columns else 0
        total_obitos = df_estados['last_available_deaths'].sum() if 'last_available_deaths' in df_estados.columns else 0
        casos_novos = df_estados['new_confirmed'].sum() if 'new_confirmed' in df_estados.columns else 0
        obitos_novos = df_estados['new_deaths'].sum() if 'new_deaths' in df_estados.columns else 0
        
        print(f"   • Total casos: {total_casos:,}")
        print(f"   • Total óbitos: {total_obitos:,}")
        print(f"   • Casos novos: {casos_novos:,}")
        print(f"   • Óbitos novos: {obitos_novos:,}")
        
        # Top 5 estados
        if 'state' in df_estados.columns and 'last_available_confirmed' in df_estados.columns:
            top_estados = df_estados.sort_values('last_available_confirmed', ascending=False).head(5)
            print(f"   • Top 5 estados:")
            for _, row in top_estados.iterrows():
                print(f"     - {row['state']}: {row['last_available_confirmed']:,} casos")
    else:
        print("❌ Nenhum dado por estado carregado")
    
    # Testar dados históricos
    print("\n📈 Testando dados históricos...")
    df_historico = client.get_brasil_historical_data()
    
    if df_historico is not None and not df_historico.empty:
        print(f"✅ Dados históricos carregados: {len(df_historico)} registros")
        print(f"   • Colunas: {list(df_historico.columns)}")
        print(f"   • Período: {df_historico['date'].min()} a {df_historico['date'].max()}")
        
        # Dados mais recentes
        ultimo_registro = df_historico.tail(1).iloc[0]
        print(f"   • Últimos dados:")
        if 'confirmed' in df_historico.columns:
            print(f"     - Casos confirmados: {ultimo_registro['confirmed']:,}")
        if 'deaths' in df_historico.columns:
            print(f"     - Óbitos: {ultimo_registro['deaths']:,}")
    else:
        print("❌ Nenhum dado histórico carregado")
    
    # Simular função do dashboard
    print("\n🎯 Simulando função do dashboard...")
    
    if df_estados is not None and df_historico is not None:
        print("✅ Ambos os DataFrames estão disponíveis")
        print("✅ Dashboard deve funcionar corretamente")
    else:
        print("❌ Um ou ambos os DataFrames estão None")
        print("❌ Dashboard retornará 'N/A' para todos os valores")
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO")
    print("="*60)
        
except Exception as e:
    print(f"❌ Erro no teste: {e}")
    import traceback
    traceback.print_exc()
