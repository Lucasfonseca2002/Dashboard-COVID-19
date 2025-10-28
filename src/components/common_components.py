# Componentes reutilizáveis para Streamlit
import streamlit as st
import plotly.express as px
import pandas as pd

def aplicar_layout_padrao(fig, altura=400):
    """Aplica um estilo padrão para os gráficos Plotly"""
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=altura,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def criar_card_estatistica(titulo, valor, descricao="", delta=None, delta_color="normal"):
    """Cria um card padronizado para exibir estatísticas usando Streamlit metrics
    
    Parâmetros:
    -----------
    titulo : str
        Título da métrica
    valor : str ou int
        Valor principal a ser exibido
    descricao : str
        Texto explicativo (help)
    delta : str, opcional
        Valor de variação a ser exibido
    delta_color : str
        Cor do delta ("normal", "inverse", "off")
    """
    st.metric(
        label=titulo,
        value=valor,
        delta=delta,
        delta_color=delta_color,
        help=descricao
    )

def criar_grafico_barras_horizontais(df, coluna_x, coluna_y='state_name', n_items=10, 
                                    titulo='', cor_escala='Blues', formato_texto=',.0f'):
    """Cria um gráfico de barras horizontais padronizado
    
    Parâmetros:
    -----------
    df : pandas.DataFrame
        DataFrame com os dados
    coluna_x : str
        Nome da coluna para valores do eixo X (valores numéricos)
    coluna_y : str
        Nome da coluna para valores do eixo Y (categorias)
    n_items : int
        Número de itens a exibir (top N)
    titulo : str
        Título do gráfico
    cor_escala : str
        Nome da escala de cores do Plotly (Blues, Reds, etc)
    formato_texto : str
        Formato dos textos nas barras
        
    Retorna:
    --------
    plotly.graph_objects.Figure
        Figura do Plotly pronta para exibição
    """
    fig = px.bar(
        df.nlargest(n_items, coluna_x),
        x=coluna_x,
        y=coluna_y,
        orientation='h',
        title=titulo,
        labels={coluna_x: titulo, coluna_y: ''},
        color=coluna_x,
        color_continuous_scale=cor_escala,
        text=coluna_x
    )
    fig.update_traces(texttemplate=f'%{{text:{formato_texto}}}', textposition='outside')
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False,
        margin=dict(l=150)
    )
    return aplicar_layout_padrao(fig, altura=400)

def criar_ranking_lista(df, coluna_score, coluna_titulo='state_name', 
                       maior=True, metricas=None):
    """Cria uma lista formatada para rankings usando Streamlit
    
    Parâmetros:
    -----------
    df : pandas.DataFrame
        DataFrame com os dados
    coluna_score : str
        Nome da coluna com o valor de score para ordenar
    coluna_titulo : str
        Nome da coluna com o texto a ser exibido como título
    maior : bool
        Se True, mostra os maiores valores. Se False, os menores
    metricas : list
        Lista de colunas adicionais para exibir como métricas
    """
    if metricas is None:
        metricas = ['mortality_rate', 'affected_population_pct']
    
    if maior:
        dados = df.nlargest(5, coluna_score).copy()
    else:
        dados = df.nsmallest(5, coluna_score).copy()
    
    for idx, (_, row) in enumerate(dados.iterrows(), 1):
        titulo = str(row.get(coluna_titulo, f"Item {idx}"))
        score = float(row.get(coluna_score, 0))
        
        metricas_texto = []
        for metrica in metricas:
            if metrica in row:
                valor = float(row.get(metrica, 0))
                nome = metrica.replace('_', ' ').title()
                metricas_texto.append(f"{nome}: {valor:.1f}%")
        
        texto_metrica = " | ".join(metricas_texto)
        
        st.write(f"**{idx}. {titulo}**")
        st.write(f"Score: {score:.2f} | {texto_metrica}")
        st.write("---")

def criar_header(titulo, subtitulo=""):
    """Cria um cabeçalho padronizado para dashboards
    
    Parâmetros:
    -----------
    titulo : str
        Título principal do dashboard
    subtitulo : str
        Subtítulo ou descrição do dashboard
    """
    st.title(titulo)
    if subtitulo:
        st.markdown(f"*{subtitulo}*")
    st.divider()

def criar_secao_titulo(titulo, icone=""):
    """Cria um título de seção padronizado
    
    Parâmetros:
    -----------
    titulo : str
        Título da seção
    icone : str
        Emoji ou ícone para exibir ao lado do título
    """
    titulo_texto = f"{icone} {titulo}" if icone else titulo
    st.subheader(titulo_texto)

def exibir_grafico(fig, titulo="", use_container_width=True):
    """Exibe um gráfico Plotly no Streamlit
    
    Parâmetros:
    -----------
    fig : plotly.graph_objects.Figure
        Figura do Plotly
    titulo : str
        Título opcional para exibir acima do gráfico
    use_container_width : bool
        Se deve usar a largura total do container
    """
    if titulo:
        st.subheader(titulo)
    st.plotly_chart(fig, use_container_width=use_container_width)

def criar_colunas_metricas(metricas_dados, num_colunas=None):
    """Cria colunas com métricas usando Streamlit
    
    Parâmetros:
    -----------
    metricas_dados : list
        Lista de dicionários com dados das métricas
        Cada dicionário deve ter: {'titulo': str, 'valor': str/int, 'descricao': str, 'delta': str}
    num_colunas : int, opcional
        Número de colunas. Se None, usa o número de métricas
    """
    if num_colunas is None:
        num_colunas = len(metricas_dados)
    
    cols = st.columns(num_colunas)
    
    for i, metrica in enumerate(metricas_dados):
        with cols[i % num_colunas]:
            criar_card_estatistica(
                titulo=metrica.get('titulo', ''),
                valor=metrica.get('valor', ''),
                descricao=metrica.get('descricao', ''),
                delta=metrica.get('delta', None)
            )