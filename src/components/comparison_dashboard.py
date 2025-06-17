# Dashboard comparativo

import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.data.api_client import COVID19APIClient
from src.components.common_components import aplicar_layout_padrao

def create_comparison_dashboard():
    """Cria o dashboard de comparação mundial"""
    
    return html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("COVID-19 - Comparação Mundial", className="text-center mb-4"),
                html.P("Análise comparativa entre o Brasil e outros países", 
                      className="text-center text-muted mb-4"),
                html.Hr()
            ])
        ]),
        
        # Seleção de países para comparação
        dbc.Row([
            dbc.Col([
                html.H3("🌎 Selecione países para comparar com o Brasil", className="text-primary mb-3"),
                dcc.Dropdown(
                    id='paises-dropdown',
                    options=[
                        {'label': 'Estados Unidos', 'value': 'USA'},
                        {'label': 'Índia', 'value': 'India'},
                        {'label': 'Rússia', 'value': 'Russia'},
                        {'label': 'Reino Unido', 'value': 'UK'},
                        {'label': 'França', 'value': 'France'},
                        {'label': 'Itália', 'value': 'Italy'},
                        {'label': 'Alemanha', 'value': 'Germany'},
                        {'label': 'Espanha', 'value': 'Spain'},
                        {'label': 'Argentina', 'value': 'Argentina'},
                        {'label': 'Colômbia', 'value': 'Colombia'},
                        {'label': 'México', 'value': 'Mexico'},
                        {'label': 'Peru', 'value': 'Peru'},
                        {'label': 'África do Sul', 'value': 'South Africa'},
                        {'label': 'China', 'value': 'China'},
                        {'label': 'Japão', 'value': 'Japan'}
                    ],
                    value=['USA', 'India', 'France', 'Argentina'],
                    multi=True
                ),
                html.Div([
                    dbc.Button(
                        "Atualizar Comparação", 
                        id="btn-atualizar-comparacao", 
                        color="primary", 
                        className="mt-2"
                    )
                ], className="d-grid gap-2")
            ], width=12)
        ], className="mb-4"),
        
        # Top países (não inclui Brasil)
        dbc.Row([
            dbc.Col([
                html.H3("🗺️ Top Países Mais Afetados", className="text-primary mb-3")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Top 5 Países - Casos Confirmados", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-comparacao-casos")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Top 5 Países - Óbitos", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-comparacao-obitos")
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Taxa de Mortalidade por País (%)", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-comparacao-mortalidade")
                    ])
                ])
            ], width=12),
        ], className="mb-4"),
        
        # Comparação com o Brasil
        dbc.Row([
            dbc.Col([
                html.H3(" Brasil vs. Outros Países", className="text-primary mb-3")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Casos por Milhão de Habitantes", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-comparacao-casos-per-million")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Óbitos por Milhão de Habitantes", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-comparacao-obitos-per-million")
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Testes por Milhão de Habitantes", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-comparacao-testes")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Taxa de Casos Ativos (%)", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-comparacao-ativos")
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        # Gráfico radar para comparação multidimensional
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Comparação Multidimensional entre Países", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-radar-comparacao")
                    ])
                ])
            ], width=12),
        ], className="mb-4"),
        
        # Intervalo para atualização
        dcc.Interval(
            id='interval-comparacao',
            interval=300000,  # 5 minutos
            n_intervals=0
        )
    ])

@callback(
    [Output('grafico-comparacao-casos', 'figure'),
     Output('grafico-comparacao-obitos', 'figure'),
     Output('grafico-comparacao-mortalidade', 'figure')],
    [Input('interval-comparacao', 'n_intervals')]
)
def update_top_countries(n):
    """Atualiza os gráficos de top países"""
    
    client = COVID19APIClient()
    df_world = client.get_world_top_countries(5)
    
    if df_world is None:
        return {}, {}, {}
    
    # Gráfico de casos
    fig_casos = px.bar(
        df_world,
        x='country',
        y='cases',
        title='Top 5 Países - Casos Confirmados (Excluindo Brasil)',
        labels={'cases': 'Casos Confirmados', 'country': 'País'}
    )
    aplicar_layout_padrao(fig_casos)
    
    # Gráfico de óbitos
    fig_obitos = px.bar(
        df_world,
        x='country',
        y='deaths',
        title='Top 5 Países - Óbitos',
        labels={'deaths': 'Óbitos', 'country': 'País'},
        color_discrete_sequence=['red']
    )
    aplicar_layout_padrao(fig_obitos)
    
    # Taxa de mortalidade
    df_world['mortality_rate'] = (df_world['deaths'] / df_world['cases']) * 100
    
    fig_mortalidade = px.bar(
        df_world,
        x='country',
        y='mortality_rate',
        title='Taxa de Mortalidade por País (%)',
        labels={'mortality_rate': 'Taxa de Mortalidade (%)', 'country': 'País'},
        color_discrete_sequence=['orange']
    )
    aplicar_layout_padrao(fig_mortalidade)
    
    return fig_casos, fig_obitos, fig_mortalidade

@callback(
    [Output('grafico-comparacao-casos-per-million', 'figure'),
     Output('grafico-comparacao-obitos-per-million', 'figure'),
     Output('grafico-comparacao-testes', 'figure'),
     Output('grafico-comparacao-ativos', 'figure'),
     Output('grafico-radar-comparacao', 'figure')],
    [Input('btn-atualizar-comparacao', 'n_clicks')],
    [State('paises-dropdown', 'value')]
)
def update_countries_comparison(n_clicks, countries):
    """Atualiza os gráficos de comparação com o Brasil"""
    if n_clicks is None and countries is None:
        # Valores padrão para o primeiro carregamento
        countries = ['USA', 'India', 'France', 'Argentina']
    
    if not countries:
        # Garante que pelo menos um país esteja selecionado
        countries = ['USA']
        
    client = COVID19APIClient()
    df_comparison = client.get_world_countries_comparison(countries)
    
    if df_comparison is None:
        return {}, {}, {}, {}, {}
    
    # Destacar o Brasil
    df_comparison['pais_destaque'] = df_comparison['country'].apply(
        lambda x: 'Brasil' if x == 'Brazil' else 'Outros países'
    )
    
    # Cores personalizadas para destacar o Brasil
    color_map = {'Brasil': '#009c3b', 'Outros países': '#4682b4'}
    
    # Gráfico de casos por milhão
    fig_casos_pm = px.bar(
        df_comparison,
        x='country',
        y='cases_per_million',
        title='Casos por Milhão de Habitantes',
        labels={'cases_per_million': 'Casos por Milhão', 'country': 'País'},
        color='pais_destaque',
        color_discrete_map=color_map
    )
    aplicar_layout_padrao(fig_casos_pm)
    
    # Gráfico de óbitos por milhão
    fig_obitos_pm = px.bar(
        df_comparison,
        x='country',
        y='deaths_per_million',
        title='Óbitos por Milhão de Habitantes',
        labels={'deaths_per_million': 'Óbitos por Milhão', 'country': 'País'},
        color='pais_destaque',
        color_discrete_map=color_map
    )
    aplicar_layout_padrao(fig_obitos_pm)
    
    # Gráfico de testes por milhão
    fig_testes = px.bar(
        df_comparison,
        x='country',
        y='tests_per_million',
        title='Testes por Milhão de Habitantes',
        labels={'tests_per_million': 'Testes por Milhão', 'country': 'País'},
        color='pais_destaque',
        color_discrete_map=color_map
    )
    aplicar_layout_padrao(fig_testes)
    
    # Gráfico de casos ativos (%)
    fig_ativos = px.bar(
        df_comparison,
        x='country',
        y='active_rate',
        title='Taxa de Casos Ativos (%)',
        labels={'active_rate': 'Casos Ativos (%)', 'country': 'País'},
        color='pais_destaque',
        color_discrete_map=color_map
    )
    aplicar_layout_padrao(fig_ativos)
    
    # Criar gráfico radar para comparação multidimensional
    # Preparar dados para o radar chart - normalizando valores
    radar_metrics = ['cases_per_million', 'deaths_per_million', 
                   'tests_per_million', 'active_rate', 'mortality_rate']
    
    # Normalizar cada métrica para valores entre 0 e 1
    radar_df = df_comparison.copy()
    for metric in radar_metrics:
        max_value = radar_df[metric].max()
        if max_value > 0:  # Evitar divisão por zero
            radar_df[f'{metric}_norm'] = radar_df[metric] / max_value
    
    # Criar gráfico radar
    fig_radar = go.Figure()
    
    # Adicionar um traço para cada país
    for idx, row in radar_df.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row[f'{m}_norm'] for m in radar_metrics],
            theta=['Casos/milhão', 'Óbitos/milhão', 'Testes/milhão', 'Taxa de ativos', 'Taxa de mortalidade'],
            fill='toself',
            name=row['country'],
            line_color='#009c3b' if row['country'] == 'Brazil' else None
        ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        title="Comparação Multidimensional entre Países",
        height=500
    )
    
    return fig_casos_pm, fig_obitos_pm, fig_testes, fig_ativos, fig_radar
