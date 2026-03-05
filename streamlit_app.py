# Dashboard COVID-19 - Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Verificação de saúde para Streamlit Cloud
def health_check():
    """Verificação de saúde simples para o Streamlit Cloud"""
    try:
        # Teste básico de funcionalidade
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

# Importações condicionais para evitar falhas de inicialização
try:
    from src.data.api_client import COVID19APIClient
    from src.data.data_processor import (
        get_fallback_brasil_data, get_fallback_world_data, get_fallback_countries_data
    )
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

@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_brasil_data():
    """Carrega dados do Brasil com cache e tratamento de erro robusto"""
    try:
        client = COVID19APIClient()
        data = client.get_brasil_data()
        if data is not None and not data.empty:
            return data
        else:
            st.info("📊 Exibindo dados de demonstração (API indisponível)")
            # Retorna dados de fallback se a API falhar
            return get_fallback_brasil_data()
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados do Brasil: {str(e)}")
        st.info("📊 Exibindo dados de demonstração (API indisponível)")
        return get_fallback_brasil_data()

@st.cache_data(ttl=300)
def load_world_data(limit=10):
    """Carrega dados mundiais com cache e tratamento de erro robusto"""
    try:
        client = COVID19APIClient()
        data = client.get_world_top_countries(limit)
        if data is not None and not data.empty:
            return data
        else:
            st.info("🌍 Exibindo dados de demonstração mundiais (API indisponível)")
            # Retorna dados de fallback se a API falhar
            return get_fallback_world_data(limit)
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados mundiais: {str(e)}")
        st.info("🌍 Exibindo dados de demonstração mundiais (API indisponível)")
        return get_fallback_world_data(limit)

@st.cache_data(ttl=300)
def load_countries_data(countries):
    """Carrega dados de países específicos com cache e tratamento de erro robusto"""
    try:
        client = COVID19APIClient()
        data = client.get_world_countries_data(countries)
        if data is not None and not data.empty:
            return data
        else:
            st.info(f"🌍 Exibindo dados de demonstração para {', '.join(countries)} (API indisponível)")
            # Retorna dados de fallback se a API falhar
            return get_fallback_countries_data(countries)
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados de países específicos: {str(e)}")
        st.info(f"🌍 Exibindo dados de demonstração para {', '.join(countries)} (API indisponível)")
        return get_fallback_countries_data(countries)

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
    st.header("🌍 COVID-19 - Comparação Mundial")
    st.markdown("Análise comparativa entre o Brasil e outros países")
    
    # Seleção de países
    st.subheader("Selecione países para comparar com o Brasil")
    
    paises_opcoes = [
        'USA', 'India', 'Russia', 'UK', 'France', 'Italy', 'Germany', 
        'Spain', 'Argentina', 'Colombia', 'Mexico', 'Peru', 'South Africa', 
        'China', 'Japan'
    ]
    
    paises_selecionados = st.multiselect(
        "Países:",
        paises_opcoes,
        default=['USA', 'India', 'France', 'Argentina']
    )
    
    if not paises_selecionados:
        st.warning("Selecione pelo menos um país para comparação.")
        return
    
    # Carregar dados
    with st.spinner("Carregando dados mundiais..."):
        df_world = load_world_data(10)
        df_countries = load_countries_data(paises_selecionados)
    
    if df_world is None or df_world.empty:
        st.error("❌ Não foi possível carregar os dados mundiais.")
        return
    
    # Top países (excluindo Brasil)
    st.subheader("🏆 Top 5 Países (excluindo Brasil)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Casos Confirmados**")
        fig_casos = px.bar(
            df_world.head(5),
            x='country',
            y='cases',
            labels={'cases': 'Casos', 'country': 'País'},
            color='cases',
            color_continuous_scale='Blues'
        )
        fig_casos.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_casos, use_container_width=True)
    
    with col2:
        st.markdown("**Óbitos**")
        fig_obitos = px.bar(
            df_world.head(5),
            x='country',
            y='deaths',
            labels={'deaths': 'Óbitos', 'country': 'País'},
            color='deaths',
            color_continuous_scale='Reds'
        )
        fig_obitos.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_obitos, use_container_width=True)
    
    with col3:
        st.markdown("**Taxa de Mortalidade**")
        df_world['mortality_rate'] = (df_world['deaths'] / df_world['cases'] * 100).fillna(0)
        fig_mortalidade = px.bar(
            df_world.head(5),
            x='country',
            y='mortality_rate',
            labels={'mortality_rate': 'Taxa (%)', 'country': 'País'},
            color='mortality_rate',
            color_continuous_scale='Oranges'
        )
        fig_mortalidade.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_mortalidade, use_container_width=True)
    
    # Comparação com países selecionados
    if df_countries is not None and not df_countries.empty:
        st.subheader("📈 Comparação Detalhada")
        
        # Adicionar Brasil aos dados
        df_brasil = load_brasil_data()
        if df_brasil is not None and not df_brasil.empty:
            brasil_data = {
                'country': 'Brazil',
                'cases': df_brasil['last_available_confirmed'].sum(),
                'deaths': df_brasil['last_available_deaths'].sum(),
                'casesPerOneMillion': df_brasil['last_available_confirmed'].sum() / 215.3,  # População em milhões
                'deathsPerOneMillion': df_brasil['last_available_deaths'].sum() / 215.3
            }
            
            # Combinar dados
            df_comparison = pd.concat([
                df_countries,
                pd.DataFrame([brasil_data])
            ], ignore_index=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Casos por Milhão de Habitantes**")
                fig_per_million = px.bar(
                    df_comparison,
                    x='country',
                    y='casesPerOneMillion',
                    labels={'casesPerOneMillion': 'Casos por Milhão', 'country': 'País'},
                    color='casesPerOneMillion',
                    color_continuous_scale='Viridis'
                )
                fig_per_million.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_per_million, use_container_width=True)
            
            with col2:
                st.markdown("**Óbitos por Milhão de Habitantes**")
                fig_deaths_per_million = px.bar(
                    df_comparison,
                    x='country',
                    y='deathsPerOneMillion',
                    labels={'deathsPerOneMillion': 'Óbitos por Milhão', 'country': 'País'},
                    color='deathsPerOneMillion',
                    color_continuous_scale='Reds'
                )
                fig_deaths_per_million.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_deaths_per_million, use_container_width=True)

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

def main():
    """Função principal da aplicação"""
    
    # Título principal
    st.title("🦠 Dashboard COVID-19")
    st.markdown("Análise de dados da COVID-19 no Brasil e no mundo")
    
    # Sidebar para navegação
    st.sidebar.title("Navegação")
    page = st.sidebar.selectbox(
        "Escolha uma página:",
        ["Brasil", "Análises Avançadas", "Comparação Mundial"]
    )
    
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