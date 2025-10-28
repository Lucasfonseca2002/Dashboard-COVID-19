# Dashboard COVID-19 - Streamlit

import streamlit as st
import sys
import os

# Verificação de saúde para Streamlit Cloud
def health_check():
    """Verificação de saúde simples para o Streamlit Cloud"""
    try:
        # Teste básico de funcionalidade
        import pandas as pd
        test_df = pd.DataFrame({'test': [1, 2, 3]})
        return True
    except Exception:
        return False

# Inicialização rápida para evitar timeouts
if not health_check():
    st.error("❌ Falha na verificação de saúde da aplicação")
    st.stop()

# Adicionar o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Lazy imports - carregamento sob demanda
_pandas = None
_plotly_express = None
_plotly_go = None
_plotly_subplots = None

def get_pandas():
    """Carregamento lazy do pandas"""
    global _pandas
    if _pandas is None:
        import pandas as pd
        _pandas = pd
    return _pandas

def get_plotly_express():
    """Carregamento lazy do plotly express"""
    global _plotly_express
    if _plotly_express is None:
        import plotly.express as px
        _plotly_express = px
    return _plotly_express

def get_plotly_go():
    """Carregamento lazy do plotly graph objects"""
    global _plotly_go
    if _plotly_go is None:
        import plotly.graph_objects as go
        _plotly_go = go
    return _plotly_go

def get_plotly_subplots():
    """Carregamento lazy do plotly subplots"""
    global _plotly_subplots
    if _plotly_subplots is None:
        from plotly.subplots import make_subplots
        _plotly_subplots = make_subplots
    return _plotly_subplots

# Importações condicionais para evitar falhas de inicialização
try:
    from src.data.api_client import COVID19APIClient
    from src.components.advanced_analytics import (
        create_time_series_charts, create_moving_averages_chart, 
        create_per_capita_analysis, create_brazil_charts, create_regional_analysis
    )
    IMPORTS_SUCCESS = True
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {str(e)}")
    IMPORTS_SUCCESS = False

# Configuração da página
st.set_page_config(
    page_title="Dashboard COVID-19",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificação adicional de saúde
if not IMPORTS_SUCCESS:
    st.error("❌ Falha ao carregar componentes da aplicação")
    st.info("🔄 Tente recarregar a página em alguns instantes")
    st.stop()

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #007bff;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    .danger { border-left-color: #dc3545; }
    .danger .metric-value { color: #dc3545; }
    .warning { border-left-color: #ffc107; }
    .warning .metric-value { color: #ffc107; }
    .success { border-left-color: #28a745; }
    .success .metric-value { color: #28a745; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=1800, max_entries=3)  # Cache por 30 minutos, máximo 3 entradas
def load_brasil_data():
    """Carrega dados do Brasil com cache e tratamento de erro robusto"""
    try:
        client = COVID19APIClient()
        data = client.get_brasil_data()
        if data is not None and not data.empty:
            return data
        else:
            # Retorna dados de fallback se a API falhar
            return get_fallback_brasil_data()
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados do Brasil: {str(e)}")
        return get_fallback_brasil_data()

@st.cache_data(ttl=1800, max_entries=5)  # Cache por 30 minutos, máximo 5 entradas
def load_world_data(limit=10):
    """Carrega dados mundiais com cache e tratamento de erro robusto"""
    try:
        client = COVID19APIClient()
        data = client.get_world_top_countries(limit)
        if data is not None and not data.empty:
            return data
        else:
            # Retorna dados de fallback se a API falhar
            return get_fallback_world_data(limit)
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados mundiais: {str(e)}")
        return get_fallback_world_data(limit)

@st.cache_data(ttl=1800, max_entries=10)  # Cache por 30 minutos, máximo 10 entradas
def load_countries_data(countries):
    """Carrega dados de países específicos com cache e tratamento de erro robusto"""
    try:
        client = COVID19APIClient()
        data = client.get_world_countries_data(countries)
        if data is not None and not data.empty:
            return data
        else:
            # Retorna dados de fallback se a API falhar
            return get_fallback_countries_data(countries)
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados de países específicos: {str(e)}")
        return get_fallback_countries_data(countries)

def get_fallback_brasil_data():
    """Retorna dados de fallback para o Brasil quando a API não está disponível"""
    pd = get_pandas()
    
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
    
    df = pd.DataFrame(fallback_data)
    st.info("📊 Exibindo dados de demonstração (API indisponível)")
    return df

def get_fallback_world_data(limit=10):
    """Retorna dados de fallback para países quando a API não está disponível"""
    pd = get_pandas()
    
    # Dados simulados baseados em dados reais aproximados
    fallback_data = {
        'country': ['USA', 'India', 'France', 'Germany', 'Iran', 'Russia', 'South Korea', 'Japan', 'Italy', 'Turkey'],
        'cases': [103000000, 45000000, 38000000, 38000000, 7500000, 22000000, 31000000, 33000000, 26000000, 17000000],
        'deaths': [1120000, 530000, 174000, 174000, 145000, 400000, 34000, 74000, 190000, 102000],
        'todayCases': [15000, 8000, 12000, 9000, 500, 3000, 2500, 4000, 3500, 2000],
        'todayDeaths': [150, 80, 45, 35, 15, 25, 5, 20, 18, 12],
        'population': [331000000, 1380000000, 65000000, 83000000, 84000000, 146000000, 51000000, 126000000, 60000000, 84000000]
    }
    
    df = pd.DataFrame(fallback_data).head(limit)
    st.info("🌍 Exibindo dados de demonstração mundiais (API indisponível)")
    return df

def get_fallback_countries_data(countries):
    """Retorna dados de fallback para países específicos quando a API não está disponível"""
    pd = get_pandas()
    
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
        df = pd.DataFrame(fallback_data)
        st.info(f"🌍 Exibindo dados de demonstração para {', '.join(countries)} (API indisponível)")
        return df
    else:
        return pd.DataFrame()

def format_number(num):
    """Formata números com separadores de milhares"""
    return f"{num:,}".replace(",", ".")

def create_metric_card(label, value, css_class=""):
    """Cria um card de métrica personalizado"""
    return f"""
    <div class="metric-card {css_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

def dashboard_brasil():
    """Dashboard específico do Brasil"""
    st.header("COVID-19 - Brasil")
    st.markdown("Análise completa dos dados da COVID-19 no território brasileiro")
    
    # Carregar dados
    with st.spinner("Carregando dados do Brasil..."):
        df_estados = load_brasil_data()
    
    if df_estados is None or df_estados.empty:
        st.error("❌ Não foi possível carregar os dados do Brasil. Verifique a conexão com a API.")
        return
    
    # Calcular métricas nacionais
    total_casos = df_estados['last_available_confirmed'].sum()
    total_obitos = df_estados['last_available_deaths'].sum()
    casos_novos = df_estados['new_confirmed'].sum() if 'new_confirmed' in df_estados.columns else 0
    obitos_novos = df_estados['new_deaths'].sum() if 'new_deaths' in df_estados.columns else 0
    
    # Métricas calculadas
    taxa_mortalidade = (total_obitos / total_casos * 100) if total_casos > 0 else 0
    client = COVID19APIClient()
    populacao_afetada = (total_casos / client.brasil_populacao * 100) if total_casos > 0 else 0
    incidencia = (total_casos / client.brasil_populacao * 100000) if total_casos > 0 else 0
    
    # Cards de métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Total de Casos Confirmados", 
            format_number(total_casos)
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Total de Óbitos", 
            format_number(total_obitos),
            "danger"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Taxa de Mortalidade", 
            f"{taxa_mortalidade:.2f}%",
            "warning"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "População Afetada", 
            f"{populacao_afetada:.2f}%",
            "success"
        ), unsafe_allow_html=True)
    
    # Segunda linha de métricas
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Casos Novos", format_number(casos_novos))
    
    with col6:
        st.metric("Óbitos Novos", format_number(obitos_novos))
    
    with col7:
        st.metric("Incidência (por 100k hab)", f"{incidencia:,.0f}")
    
    with col8:
        if 'date' in df_estados.columns:
            max_date = df_estados['date'].max()
            # Verificar se é string ou datetime
            if isinstance(max_date, str):
                try:
                    # Tentar converter string para datetime e depois formatar
                    from datetime import datetime
                    date_obj = pd.to_datetime(max_date)
                    ultima_data = date_obj.strftime('%d/%m/%Y')
                except:
                    # Se não conseguir converter, usar a string diretamente
                    ultima_data = max_date
            else:
                # Se já é datetime, usar strftime normalmente
                ultima_data = max_date.strftime('%d/%m/%Y')
        else:
            ultima_data = "N/A"
        st.metric("Última Atualização", ultima_data)
    
    st.markdown("---")
    
    # Gráficos
    st.subheader("📊 Análises por Estados")
    
    # Top 10 Estados
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top 10 Estados - Casos Confirmados**")
        top_casos = df_estados.nlargest(10, 'last_available_confirmed')
        fig_casos = px.bar(
            top_casos,
            x='last_available_confirmed',
            y='state_name' if 'state_name' in top_casos.columns else 'state',
            orientation='h',
            labels={'last_available_confirmed': 'Casos Confirmados', 'state_name': 'Estado'},
            color='last_available_confirmed',
            color_continuous_scale='Blues'
        )
        fig_casos.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_casos, use_container_width=True)
    
    with col2:
        st.markdown("**Top 10 Estados - Óbitos**")
        top_obitos = df_estados.nlargest(10, 'last_available_deaths')
        fig_obitos = px.bar(
            top_obitos,
            x='last_available_deaths',
            y='state_name' if 'state_name' in top_obitos.columns else 'state',
            orientation='h',
            labels={'last_available_deaths': 'Óbitos', 'state_name': 'Estado'},
            color='last_available_deaths',
            color_continuous_scale='Reds'
        )
        fig_obitos.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_obitos, use_container_width=True)
    
    # Taxa de mortalidade por estado
    st.markdown("**Taxa de Mortalidade por Estado**")
    df_estados['taxa_mortalidade'] = (df_estados['last_available_deaths'] / df_estados['last_available_confirmed'] * 100).fillna(0)
    top_mortalidade = df_estados.nlargest(15, 'taxa_mortalidade')
    
    fig_mortalidade = px.bar(
        top_mortalidade,
        x='state_name' if 'state_name' in top_mortalidade.columns else 'state',
        y='taxa_mortalidade',
        labels={'taxa_mortalidade': 'Taxa de Mortalidade (%)', 'state_name': 'Estado'},
        color='taxa_mortalidade',
        color_continuous_scale='Oranges'
    )
    fig_mortalidade.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_mortalidade, use_container_width=True)

def dashboard_comparacao():
    """Dashboard de comparação mundial"""
    st.header("🌍 Comparação Mundial")
    st.markdown("Compare dados da COVID-19 entre diferentes países")
    
    # Seleção de países
    paises_disponiveis = [
        'USA', 'India', 'France', 'Germany', 'Iran', 'Russia', 
        'South Korea', 'Japan', 'Italy', 'Turkey', 'UK', 'China'
    ]
    
    paises_selecionados = st.multiselect(
        "Selecione os países para comparação:",
        paises_disponiveis,
        default=['USA', 'India', 'France', 'Germany']
    )
    
    if paises_selecionados:
        # Carregar dados dos países selecionados
        with st.spinner("Carregando dados dos países..."):
            df_paises = load_countries_data(paises_selecionados)
        
        if df_paises is not None and not df_paises.empty:
            # Exibir dados em tabela
            st.subheader("📊 Dados Comparativos")
            st.dataframe(df_paises)
            
            # Gráficos comparativos
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Casos Totais")
                if 'cases' in df_paises.columns:
                    px = get_plotly_express()
                    fig = px.bar(df_paises, x='country', y='cases', 
                               title="Casos Totais por País")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("💀 Óbitos Totais")
                if 'deaths' in df_paises.columns:
                    px = get_plotly_express()
                    fig = px.bar(df_paises, x='country', y='deaths', 
                               title="Óbitos Totais por País", color_discrete_sequence=['red'])
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ Não foi possível carregar os dados dos países selecionados.")
    else:
        st.info("👆 Selecione pelo menos um país para visualizar os dados.")

# Função de monitoramento de memória
def get_memory_usage():
    """Obtém uso de memória atual (simplificado para Streamlit Cloud)"""
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024  # Converter para MB
        return memory_mb
    except ImportError:
        # Se psutil não estiver disponível, retorna None
        return None
    except Exception:
        return None

def show_memory_debug():
    """Mostra informações de debug de memória se habilitado"""
    if st.sidebar.checkbox("🔍 Debug de Memória", value=False):
        memory_usage = get_memory_usage()
        if memory_usage:
            st.sidebar.metric("Uso de Memória", f"{memory_usage:.1f} MB")
            if memory_usage > 800:  # Alerta se próximo do limite de 1GB
                st.sidebar.warning("⚠️ Uso de memória alto!")
        else:
            st.sidebar.info("Monitoramento de memória não disponível")

def main():
    """Função principal do dashboard"""
    st.title("🦠 Dashboard COVID-19")
    st.markdown("Análise de dados da COVID-19 no Brasil e no mundo")
    
    # Sidebar para navegação
    st.sidebar.title("Navegação")
    page = st.sidebar.selectbox(
        "Escolha uma página:",
        ["Brasil", "Análises Avançadas", "Comparação Mundial"]
    )
    
    # Monitoramento de memória (debug)
    show_memory_debug()
    
    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Sobre o Dashboard")
    st.sidebar.markdown("""
    Este dashboard apresenta dados atualizados sobre a COVID-19:
    
    **🇧🇷 Brasil**: Análise detalhada por estados
    **📈 Análises Avançadas**: Séries temporais, mapas e indicadores
    **🌍 Mundial**: Comparação entre países
    
    **Fontes de dados:**
    - Brasil.io (dados nacionais)
    - Disease.sh (dados mundiais)
    """)
    
    # Renderizar página selecionada
    if page == "Brasil":
        dashboard_brasil()
    elif page == "Análises Avançadas":
        dashboard_analises_avancadas()
    elif page == "Comparação Mundial":
        dashboard_comparacao()
    
    # Footer
    st.markdown("---")
    st.markdown("*Dashboard desenvolvido com Streamlit | Dados atualizados automaticamente*")

if __name__ == "__main__":
    main()

def dashboard_analises_avancadas():
    """Dashboard com análises avançadas dos dados de COVID-19 do Brasil"""
    
    st.header("📈 Análises Avançadas - COVID-19 Brasil")
    st.markdown("Análises detalhadas com séries temporais, mapas interativos e indicadores avançados")
    
    # Inicializar cliente da API
    api_client = COVID19APIClient()
    
    # Carregar dados
    with st.spinner("Carregando dados..."):
        try:
            # Dados atuais do Brasil
            brasil_data = api_client.get_brasil_data()
            
            # Dados históricos (últimos 90 dias)
            historical_data = api_client.get_brasil_historical_data(limit=2000)
            
            # Séries temporais
            time_series_data = api_client.get_brasil_time_series(days=90)
            
            # Médias móveis
            moving_averages = api_client.calculate_moving_averages(time_series_data)
            
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")
            return
    
    # Tabs para organizar as análises
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Séries Temporais", 
        "📊 Análise Comparativa", 
        "👥 Análise Per Capita", 
        "📈 Médias Móveis",
        "🗺️ Análise Regional"
    ])
    
    with tab1:
        st.subheader("Evolução Temporal da COVID-19")
        st.markdown("Acompanhe a evolução dos casos e óbitos ao longo do tempo")
        
        if time_series_data is not None and not time_series_data.empty:
            create_time_series_charts(time_series_data)
        else:
            st.warning("Dados de séries temporais não disponíveis")
    
    with tab2:
        st.subheader("Análise Comparativa entre Estados")
        st.markdown("Visualização geográfica dos dados por estado")
        
        if brasil_data is not None and not brasil_data.empty:
            create_brazil_charts(brasil_data)
        else:
            st.warning("Dados do mapa não disponíveis")
    
    with tab3:
        st.subheader("Análise Per Capita")
        st.markdown("Indicadores ajustados pela população de cada estado")
        
        if brasil_data is not None and not brasil_data.empty:
            create_per_capita_analysis(brasil_data)
        else:
            st.warning("Dados per capita não disponíveis")
    
    with tab4:
        st.subheader("Médias Móveis e Tendências")
        st.markdown("Suavização dos dados para identificar tendências")
        
        if moving_averages is not None and not moving_averages.empty:
            create_moving_averages_chart(moving_averages)
        else:
            st.warning("Dados de médias móveis não disponíveis")
    
    with tab5:
        st.subheader("Análise Regional")
        st.markdown("Comparação entre regiões do Brasil")
        
        if brasil_data is not None and not brasil_data.empty:
            create_regional_analysis(brasil_data)
        else:
            st.warning("Dados regionais não disponíveis")