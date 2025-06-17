# Componentes reutilizáveis
from dash import dcc, html
import dash_bootstrap_components as dbc
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

def criar_card_estatistica(icone, titulo, id_valor, valor_inicial="Carregando...", 
                          descricao="", cor="primary"):
    """Cria um card padronizado para exibir estatísticas
    
    Parâmetros:
    -----------
    icone : str
        Classe do ícone FontAwesome (ex: "fa-virus")
    titulo : str
        Título do card
    id_valor : str
        ID do componente que exibirá o valor principal
    valor_inicial : str
        Texto inicial a ser exibido antes dos dados carregarem
    descricao : str
        Texto explicativo abaixo do valor principal
    cor : str
        Cor do Bootstrap para o card (primary, danger, warning, etc)
    
    Retorna:
    --------
    dbc.Card
        Componente card completo
    """
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas {icone} fa-2x text-{cor} mb-2"),
                html.H4(titulo, className="card-title"),
                html.H2(valor_inicial, id=id_valor, className=f"text-{cor}"),
                html.Small(descricao, className="text-muted")
            ], className="text-center")
        ])
    ], className=f"h-100 border-{cor} shadow-sm")

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
                       maior=True, cor='danger', metricas=None):
    """Cria uma lista formatada para rankings
    
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
    cor : str
        Cor do Bootstrap para títulos (primary, danger, success, etc)
    metricas : list
        Lista de colunas adicionais para exibir como métricas
        
    Retorna:
    --------
    html.Div
        Componente Dash com a lista formatada
    """
    if metricas is None:
        metricas = ['mortality_rate', 'affected_population_pct']
    
    if maior:
        dados = df.nlargest(5, coluna_score).copy()
    else:
        dados = df.nsmallest(5, coluna_score).copy()
    
    lista_items = []
    for idx, row in dados.iterrows():
        titulo = str(row.get(coluna_titulo, f"Item {idx}"))
        score = float(row.get(coluna_score, 0))
        
        metricas_texto = []
        for metrica in metricas:
            if metrica in row:
                valor = float(row.get(metrica, 0))
                nome = metrica.replace('_', ' ').title()
                metricas_texto.append(f"{nome}: {valor:.1f}%")
        
        texto_metrica = " | ".join(metricas_texto)
        
        lista_items.append(
            html.Li([
                html.Strong(titulo, className=f"text-{cor}"),
                html.Br(),
                html.Small(
                    f"Score: {score:.2f} | {texto_metrica}",
                    className="text-muted"
                )
            ], className="mb-2")
        )
    
    return html.Div([html.Ol(lista_items)])

def criar_header(titulo, subtitulo=""):
    """Cria um cabeçalho padronizado para dashboards
    
    Parâmetros:
    -----------
    titulo : str
        Título principal do dashboard
    subtitulo : str
        Subtítulo ou descrição do dashboard
        
    Retorna:
    --------
    dbc.Row
        Componente de linha Bootstrap com o cabeçalho
    """
    return dbc.Row([
        dbc.Col([
            html.H1(titulo, className="text-center mb-4"),
            html.P(subtitulo, className="text-center text-muted mb-4"),
            html.Hr()
        ])
    ])

def criar_secao_titulo(titulo, icone=""):
    """Cria um título de seção padronizado
    
    Parâmetros:
    -----------
    titulo : str
        Título da seção
    icone : str
        Emoji ou ícone para exibir ao lado do título
        
    Retorna:
    --------
    dbc.Row
        Componente de linha Bootstrap com o título da seção
    """
    titulo_texto = f"{icone} {titulo}" if icone else titulo
    return dbc.Row([
        dbc.Col([
            html.H3(titulo_texto, className="text-primary mb-3")
        ])
    ])

def criar_card_grafico(titulo, id_grafico):
    """Cria um card padronizado para gráficos
    
    Parâmetros:
    -----------
    titulo : str
        Título do gráfico
    id_grafico : str
        ID do componente do gráfico
        
    Retorna:
    --------
    dbc.Card
        Componente card completo com título e espaço para gráfico
    """
    return dbc.Card([
        dbc.CardHeader([
            html.H5(titulo, className="mb-0")
        ]),
        dbc.CardBody([
            dcc.Graph(id=id_grafico)
        ])
    ])

def criar_linha_graficos(ids_graficos, titulos, larguras=None):
    """Cria uma linha com múltiplos gráficos
    
    Parâmetros:
    -----------
    ids_graficos : list
        Lista com os IDs dos gráficos
    titulos : list
        Lista com os títulos dos gráficos
    larguras : list, opcional
        Lista com as larguras das colunas (soma deve ser 12)
        
    Retorna:
    --------
    dbc.Row
        Componente de linha Bootstrap com os cards de gráficos
    """
    if larguras is None:
        # Distribui uniformemente
        larguras = [12 // len(ids_graficos)] * len(ids_graficos)
    
    colunas = []
    for i, (id_grafico, titulo) in enumerate(zip(ids_graficos, titulos)):
        colunas.append(
            dbc.Col([
                criar_card_grafico(titulo, id_grafico)
            ], width=larguras[i])
        )
    
    return dbc.Row(colunas, className="mb-4")