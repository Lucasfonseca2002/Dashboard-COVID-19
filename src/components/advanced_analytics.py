# Componentes de análises avançadas para COVID-19

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import json

def create_time_series_charts(df_historical, selected_states=None):
    """Cria gráficos de séries temporais"""
    if df_historical is None or df_historical.empty:
        st.error("Dados históricos não disponíveis")
        return
    
    # Filtrar estados se especificado
    if selected_states:
        df_filtered = df_historical[df_historical['state'].isin(selected_states)]
    else:
        # Pegar os 5 estados com mais casos para visualização
        top_states = df_historical.groupby('state')['last_available_confirmed'].max().nlargest(5).index.tolist()
        df_filtered = df_historical[df_historical['state'].isin(top_states)]
    
    # Gráfico de casos novos ao longo do tempo
    st.subheader("📈 Evolução de Casos Novos por Estado")
    
    fig_casos = px.line(
        df_filtered,
        x='date',
        y='new_confirmed',
        color='state',
        title='Casos Novos Diários por Estado',
        labels={'new_confirmed': 'Casos Novos', 'date': 'Data', 'state': 'Estado'}
    )
    fig_casos.update_layout(height=400)
    st.plotly_chart(fig_casos, use_container_width=True)
    
    # Gráfico de óbitos novos ao longo do tempo
    st.subheader("📉 Evolução de Óbitos por Estado")
    
    fig_obitos = px.line(
        df_filtered,
        x='date',
        y='new_deaths',
        color='state',
        title='Óbitos Diários por Estado',
        labels={'new_deaths': 'Óbitos Novos', 'date': 'Data', 'state': 'Estado'}
    )
    fig_obitos.update_layout(height=400)
    st.plotly_chart(fig_obitos, use_container_width=True)

def create_moving_averages_chart(df_with_ma):
    """Cria gráfico com médias móveis"""
    if df_with_ma is None or df_with_ma.empty:
        return
    
    st.subheader("📊 Médias Móveis (7 dias)")
    
    # Selecionar estado para análise detalhada
    states = sorted(df_with_ma['state'].unique())
    selected_state = st.selectbox("Selecione um estado para análise detalhada:", states)
    
    if selected_state:
        df_state = df_with_ma[df_with_ma['state'] == selected_state].copy()
        
        # Criar subplot com casos e óbitos
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Casos Novos vs Média Móvel', 'Óbitos vs Média Móvel'),
            vertical_spacing=0.1
        )
        
        # Casos novos
        fig.add_trace(
            go.Scatter(x=df_state['date'], y=df_state['new_confirmed'], 
                      name='Casos Diários', line=dict(color='lightblue', width=1)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df_state['date'], y=df_state['ma_cases'],
                      name='Média Móvel 7d', line=dict(color='blue', width=3)),
            row=1, col=1
        )
        
        # Óbitos
        fig.add_trace(
            go.Scatter(x=df_state['date'], y=df_state['new_deaths'], 
                      name='Óbitos Diários', line=dict(color='lightcoral', width=1)),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=df_state['date'], y=df_state['ma_deaths'],
                      name='Média Móvel 7d', line=dict(color='red', width=3)),
            row=2, col=1
        )
        
        fig.update_layout(height=600, title=f'Análise Temporal - {selected_state}')
        st.plotly_chart(fig, use_container_width=True)

def create_per_capita_analysis(df_estados):
    """Cria análises per capita"""
    if df_estados is None or df_estados.empty:
        return
    
    st.subheader("👥 Análises Per Capita")
    
    # Usar dados já calculados pela API
    df_analysis = df_estados.copy()
    
    # Calcular incidência se não estiver disponível
    if 'last_available_confirmed_per_100k_inhabitants' not in df_analysis.columns:
        df_analysis['incidencia_100k'] = (df_analysis['last_available_confirmed'] / df_analysis['estimated_population'] * 100000)
    else:
        df_analysis['incidencia_100k'] = df_analysis['last_available_confirmed_per_100k_inhabitants']
    
    # Calcular mortalidade per capita
    df_analysis['mortalidade_100k'] = (df_analysis['last_available_deaths'] / df_analysis['estimated_population'] * 100000)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Incidência por 100k Habitantes**")
        top_incidencia = df_analysis.nlargest(15, 'incidencia_100k')
        
        fig_inc = px.bar(
            top_incidencia,
            x='incidencia_100k',
            y='state',
            orientation='h',
            labels={'incidencia_100k': 'Casos por 100k hab', 'state': 'Estado'},
            color='incidencia_100k',
            color_continuous_scale='Oranges'
        )
        fig_inc.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_inc, use_container_width=True)
    
    with col2:
        st.markdown("**Mortalidade por 100k Habitantes**")
        top_mortalidade = df_analysis.nlargest(15, 'mortalidade_100k')
        
        fig_mort = px.bar(
            top_mortalidade,
            x='mortalidade_100k',
            y='state',
            orientation='h',
            labels={'mortalidade_100k': 'Óbitos por 100k hab', 'state': 'Estado'},
            color='mortalidade_100k',
            color_continuous_scale='Reds'
        )
        fig_mort.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_mort, use_container_width=True)

def create_brazil_charts(df_estados):
    """Cria visualizações por estados do Brasil usando gráficos de barras"""
    st.subheader("📊 Análise Comparativa entre Estados")
    
    if df_estados is None or df_estados.empty:
        st.error("Dados não disponíveis para criar as visualizações")
        return
    
    try:
        # Preparar dados
        df_chart = df_estados.copy()
        
        # Calcular métricas se não existirem
        if 'taxa_mortalidade' not in df_chart.columns:
            df_chart['taxa_mortalidade'] = df_chart.apply(
                lambda row: (row['last_available_deaths'] / row['last_available_confirmed'] * 100) 
                if row['last_available_confirmed'] > 0 else 0, axis=1
            )
        
        if 'incidencia_100k' not in df_chart.columns:
            if 'last_available_confirmed_per_100k_inhabitants' in df_chart.columns:
                df_chart['incidencia_100k'] = df_chart['last_available_confirmed_per_100k_inhabitants']
            else:
                df_chart['incidencia_100k'] = df_chart.apply(
                    lambda row: (row['last_available_confirmed'] / row['estimated_population'] * 100000) 
                    if row['estimated_population'] > 0 else 0, axis=1
                )
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            # Filtro por região
            regioes = {
                'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
                'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
                'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
                'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
                'Sul': ['PR', 'RS', 'SC']
            }
            
            selected_regions = st.multiselect(
                "Filtrar por Região:",
                options=list(regioes.keys()),
                default=list(regioes.keys())
            )
            
        with col2:
            # Filtro por estados específicos
            estados_filtrados = []
            for regiao in selected_regions:
                estados_filtrados.extend(regioes[regiao])
            
            selected_states = st.multiselect(
                "Filtrar por Estados:",
                options=sorted(df_chart['state'].unique()),
                default=sorted([state for state in df_chart['state'].unique() if state in estados_filtrados])
            )
        
        # Aplicar filtros
        if selected_states:
            df_filtered = df_chart[df_chart['state'].isin(selected_states)].copy()
        else:
            df_filtered = df_chart.copy()
        
        if df_filtered.empty:
            st.warning("Nenhum estado selecionado nos filtros.")
            return
        
        # Ordenar por casos confirmados para melhor visualização
        df_filtered = df_filtered.sort_values('last_available_confirmed', ascending=False)
        
        # Criar visualizações
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de casos confirmados
            fig_casos = px.bar(
                df_filtered.head(15),  # Top 15 para melhor visualização
                x='state',
                y='last_available_confirmed',
                title='Top 15 Estados - Casos Confirmados',
                labels={'last_available_confirmed': 'Casos Confirmados', 'state': 'Estado'},
                color='last_available_confirmed',
                color_continuous_scale='Blues'
            )
            fig_casos.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_casos, use_container_width=True)
            
        with col2:
            # Gráfico de óbitos
            fig_obitos = px.bar(
                df_filtered.head(15),
                x='state',
                y='last_available_deaths',
                title='Top 15 Estados - Óbitos',
                labels={'last_available_deaths': 'Óbitos', 'state': 'Estado'},
                color='last_available_deaths',
                color_continuous_scale='Reds'
            )
            fig_obitos.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_obitos, use_container_width=True)
        
        # Segunda linha de gráficos
        col3, col4 = st.columns(2)
        
        with col3:
            # Gráfico de taxa de mortalidade
            df_mortalidade = df_filtered.sort_values('taxa_mortalidade', ascending=False)
            fig_mortalidade = px.bar(
                df_mortalidade.head(15),
                x='state',
                y='taxa_mortalidade',
                title='Top 15 Estados - Taxa de Mortalidade (%)',
                labels={'taxa_mortalidade': 'Taxa de Mortalidade (%)', 'state': 'Estado'},
                color='taxa_mortalidade',
                color_continuous_scale='Oranges'
            )
            fig_mortalidade.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_mortalidade, use_container_width=True)
            
        with col4:
            # Gráfico de incidência por 100k
            df_incidencia = df_filtered.sort_values('incidencia_100k', ascending=False)
            fig_incidencia = px.bar(
                df_incidencia.head(15),
                x='state',
                y='incidencia_100k',
                title='Top 15 Estados - Incidência por 100k hab',
                labels={'incidencia_100k': 'Casos por 100k hab', 'state': 'Estado'},
                color='incidencia_100k',
                color_continuous_scale='Greens'
            )
            fig_incidencia.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_incidencia, use_container_width=True)
        
        # Estatísticas resumidas
        st.subheader("📈 Estatísticas dos Estados Selecionados")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_casos = df_filtered['last_available_confirmed'].sum()
            st.metric("Total de Casos", f"{total_casos:,.0f}")
            
        with col2:
            total_obitos = df_filtered['last_available_deaths'].sum()
            st.metric("Total de Óbitos", f"{total_obitos:,.0f}")
            
        with col3:
            taxa_media = df_filtered['taxa_mortalidade'].mean()
            st.metric("Taxa Mortalidade Média", f"{taxa_media:.2f}%")
            
        with col4:
            incidencia_media = df_filtered['incidencia_100k'].mean()
            st.metric("Incidência Média (100k)", f"{incidencia_media:,.0f}")
        
        # Tabela detalhada
        st.subheader("📋 Dados Detalhados")
        
        # Preparar dados para exibição
        df_display = df_filtered[['state', 'last_available_confirmed', 'last_available_deaths', 
                                 'taxa_mortalidade', 'incidencia_100k']].copy()
        df_display.columns = ['Estado', 'Casos Confirmados', 'Óbitos', 
                             'Taxa Mortalidade (%)', 'Incidência (100k hab)']
        
        # Formatar números
        df_display['Casos Confirmados'] = df_display['Casos Confirmados'].apply(lambda x: f"{x:,.0f}")
        df_display['Óbitos'] = df_display['Óbitos'].apply(lambda x: f"{x:,.0f}")
        df_display['Taxa Mortalidade (%)'] = df_display['Taxa Mortalidade (%)'].apply(lambda x: f"{x:.2f}")
        df_display['Incidência (100k hab)'] = df_display['Incidência (100k hab)'].apply(lambda x: f"{x:,.0f}")
        
        st.dataframe(df_display, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erro ao criar visualizações: {str(e)}")
        st.info("Verifique se os dados estão disponíveis e tente novamente.")

def create_regional_analysis(df_estados):
    """Cria análise por regiões do Brasil"""
    st.subheader("🌎 Análise por Regiões")
    
    # Definir regiões
    regioes = {
        'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
        'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
        'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
        'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
        'Sul': ['PR', 'RS', 'SC']
    }
    
    # Adicionar coluna de região
    df_regional = df_estados.copy()
    df_regional['regiao'] = df_regional['state'].map(
        {state: regiao for regiao, states in regioes.items() for state in states}
    )
    
    # Agregar dados por região
    regional_summary = df_regional.groupby('regiao').agg({
        'last_available_confirmed': 'sum',
        'last_available_deaths': 'sum',
        'estimated_population': 'sum',
        'new_confirmed': 'sum',
        'new_deaths': 'sum'
    }).reset_index()
    
    # Calcular métricas regionais
    regional_summary['taxa_mortalidade'] = (regional_summary['last_available_deaths'] / regional_summary['last_available_confirmed'] * 100)
    regional_summary['incidencia_100k'] = (regional_summary['last_available_confirmed'] / regional_summary['estimated_population'] * 100000)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_casos_regiao = px.bar(
            regional_summary,
            x='regiao',
            y='last_available_confirmed',
            title='Casos Confirmados por Região',
            labels={'last_available_confirmed': 'Casos', 'regiao': 'Região'},
            color='last_available_confirmed',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_casos_regiao, use_container_width=True)
    
    with col2:
        fig_inc_regiao = px.bar(
            regional_summary,
            x='regiao',
            y='incidencia_100k',
            title='Incidência por 100k Habitantes por Região',
            labels={'incidencia_100k': 'Casos por 100k hab', 'regiao': 'Região'},
            color='incidencia_100k',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_inc_regiao, use_container_width=True)
    
    # Tabela resumo
    st.markdown("**Resumo Regional**")
    st.dataframe(
        regional_summary[['regiao', 'last_available_confirmed', 'last_available_deaths', 
                         'taxa_mortalidade', 'incidencia_100k']].round(2),
        use_container_width=True
    )