# Dashboard específico do Brasil

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from src.data.api_client import COVID19APIClient

def create_brasil_dashboard():
    """Cria o dashboard específico do Brasil"""
    
    return html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("COVID-19 - Brasil", className="text-center mb-4"),
                html.P("Análise completa dos dados da COVID-19 no território brasileiro", 
                      className="text-center text-muted mb-4"),
                html.Hr()
            ])
        ]),
        
        # Cards com métricas principais - Primeira linha
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-virus fa-2x text-primary mb-2"),
                            html.H4("Total de Casos Confirmados", className="card-title"),
                            html.H2("Carregando...", id="total-casos-brasil", className="text-primary"),
                            html.Small("Casos acumulados", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-primary shadow-sm hover-card")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-heart-broken fa-2x text-danger mb-2"),
                            html.H4("Total de Óbitos", className="card-title"),
                            html.H2("Carregando...", id="total-obitos-brasil", className="text-danger"),
                            html.Small("Óbitos acumulados", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-danger shadow-sm")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-percentage fa-2x text-warning mb-2"),
                            html.H4("Taxa de Mortalidade Nacional", className="card-title"),
                            html.H2("Carregando...", id="taxa-mortalidade-brasil", className="text-warning"),
                            html.Small("Óbitos / Casos × 100", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-warning shadow-sm")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-users fa-2x text-info mb-2"),
                            html.H4("População Afetada", className="card-title"),
                            html.H2("Carregando...", id="populacao-afetada-brasil", className="text-info"),
                            html.Small("% da população total", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-info shadow-sm")
            ], width=3),
        ], className="mb-4"),
        
        # Cards com métricas diárias - Segunda linha
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-plus-circle fa-2x text-success mb-2"),
                            html.H4("Casos Novos (24h)", className="card-title"),
                            html.H2("Carregando...", id="casos-novos-brasil", className="text-success"),
                            html.Small("Últimas 24 horas", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-success shadow-sm")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-minus-circle fa-2x text-dark mb-2"),
                            html.H4("Óbitos Novos (24h)", className="card-title"),
                            html.H2("Carregando...", id="obitos-novos-brasil", className="text-dark"),
                            html.Small("Últimas 24 horas", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-dark shadow-sm")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-chart-line fa-2x text-secondary mb-2"),
                            html.H4("Incidência Nacional", className="card-title"),
                            html.H2("Carregando...", id="incidencia-brasil", className="text-secondary"),
                            html.Small("Casos por 100k hab.", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-secondary shadow-sm")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-calendar-alt fa-2x text-primary mb-2"),
                            html.H4("Última Atualização", className="card-title"),
                            html.H2("Carregando...", id="ultima-atualizacao-brasil", className="text-primary"),
                            html.Small("Data dos dados", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100 border-primary shadow-sm")
            ], width=3),
        ], className="mb-4"),
        
        # Seção de análises por estados
        dbc.Row([
            dbc.Col([
                html.H3("Análises por Estados", className="text-primary mb-3")
            ])
        ]),
        
        # Gráficos - Top 10 Estados
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(" Top 10 Estados - Casos Absolutos", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-top-casos-estados")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(" Top 10 Estados - Óbitos", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-top-obitos-estados")
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        # Gráficos - Taxa de mortalidade e casos per capita
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Taxa de Mortalidade por Estado", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-mortalidade-estados")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(" Casos per Capita por Estado", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-casos-per-capita")
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        # Seção de análises regionais
        dbc.Row([
            dbc.Col([
                html.H3("Análises Regionais", className="text-primary mb-3")
            ])
        ]),
        
        # Gráficos regionais
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(" Casos por Região", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-casos-regiao")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(" Densidade Populacional vs Casos", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-densidade-casos")
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        # HeatMap e Mapa
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(" HeatMap - Casos por Estado", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="heatmap-casos-estados")
                    ])
                ])
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5(" Impacto Relativo", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="grafico-impacto-relativo")
                    ])
                ])
            ], width=4),
        ], className="mb-4"),
        
        # Análises comparativas
        dbc.Row([
            dbc.Col([
                html.H3("🔍 Análises Comparativas", className="text-primary mb-3")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("🥇 Estados com Maior Impacto", className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div(id="ranking-maior-impacto")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("🥉                                                                                                                                                                                                                                                                                                                                                                                                  Impacto", className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div(id="ranking-menor-impacto")
                    ])
                ])
            ], width=6),
        ]),
        
        # Intervalo para atualização automática
        dcc.Interval(
            id='interval-brasil',
            interval=30000,  # 30 segundos
            n_intervals=0
        )
    ])

def aplicar_layout_padrao(fig, altura=400):
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=altura
    )
    return fig

# Callback principal para o dashboard do Brasil (SEM evolução temporal)
@callback(
    [Output('total-casos-brasil', 'children'),
     Output('total-obitos-brasil', 'children'),
     Output('taxa-mortalidade-brasil', 'children'),
     Output('populacao-afetada-brasil', 'children'),
     Output('casos-novos-brasil', 'children'),
     Output('obitos-novos-brasil', 'children'),
     Output('incidencia-brasil', 'children'),
     Output('ultima-atualizacao-brasil', 'children'),
     Output('grafico-top-casos-estados', 'figure'),
     Output('grafico-top-obitos-estados', 'figure'),
     Output('grafico-mortalidade-estados', 'figure'),
     Output('grafico-casos-per-capita', 'figure'),
     Output('grafico-casos-regiao', 'figure'),
     Output('grafico-densidade-casos', 'figure'),
     Output('heatmap-casos-estados', 'figure'),
     Output('grafico-impacto-relativo', 'figure'),
     Output('ranking-maior-impacto', 'children'),
     Output('ranking-menor-impacto', 'children')],
    [Input('interval-brasil', 'n_intervals')]
)
def update_brasil_dashboard(n):
    """Atualiza os dados do dashboard do Brasil"""
    
    print(f"🔄 Dashboard Brasil callback executado - iteração {n}")
    
    try:
        client = COVID19APIClient()
        
        # Dados por estado
        print(" Carregando dados por estado...")
        df_estados = client.get_brasil_data()
        
        if df_estados is None or df_estados.empty:
            print("❌ Dados não disponíveis")
            empty_fig = {'data': [], 'layout': {'title': 'Dados não disponíveis'}}
            empty_content = html.P("Dados não disponíveis")
            return ["N/A"] * 8 + [empty_fig] * 10 + [empty_content, empty_content]
        
        # Calcular métricas nacionais
        total_casos = df_estados['last_available_confirmed'].sum()
        total_obitos = df_estados['last_available_deaths'].sum()
        casos_novos = df_estados['new_confirmed'].sum() if 'new_confirmed' in df_estados.columns else 0
        obitos_novos = df_estados['new_deaths'].sum() if 'new_deaths' in df_estados.columns else 0
        
        # Métricas calculadas
        taxa_mortalidade = (total_obitos / total_casos * 100) if total_casos > 0 else 0
        populacao_afetada = (total_casos / client.brasil_populacao * 100) if total_casos > 0 else 0
        incidencia = (total_casos / client.brasil_populacao * 100000) if total_casos > 0 else 0
        
        # Data da última atualização
        ultima_data = df_estados['date'].max().strftime('%d/%m/%Y') if 'date' in df_estados.columns else "N/A"
        
        print(f" Métricas: {total_casos:,} casos, {total_obitos:,} óbitos, {taxa_mortalidade:.2f}% mortalidade")
        
        # 1. Top 10 Estados - Casos Absolutos
        fig_top_casos = px.bar(
            df_estados.nlargest(10, 'last_available_confirmed'),
            x='last_available_confirmed',
            y='state_name',
            orientation='h',
            title='',
            labels={'last_available_confirmed': 'Casos Confirmados', 'state_name': ''},
            color='last_available_confirmed',
            color_continuous_scale='Blues',
            text='last_available_confirmed'
        )
        fig_top_casos.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_top_casos.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            margin=dict(l=150)
        )
        fig_top_casos = aplicar_layout_padrao(fig_top_casos, altura=400)
        
        # 2. Top 10 Estados - Óbitos
        fig_top_obitos = px.bar(
            df_estados.nlargest(10, 'last_available_deaths'),
            x='last_available_deaths',
            y='state_name',
            orientation='h',
            title='',
            labels={'last_available_deaths': 'Óbitos', 'state_name': ''},
            color='last_available_deaths',
            color_continuous_scale='Reds',
            text='last_available_deaths'
        )
        fig_top_obitos.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_top_obitos.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            margin=dict(l=150)
        )
        fig_top_obitos = aplicar_layout_padrao(fig_top_obitos, altura=400)
        
        # 3. Taxa de Mortalidade por Estado
        fig_mortalidade = px.bar(
            df_estados.nlargest(15, 'mortality_rate'),
            x='mortality_rate',
            y='state_name',
            orientation='h',
            title='',
            labels={'mortality_rate': 'Taxa de Mortalidade (%)', 'state_name': ''},
            color='mortality_rate',
            color_continuous_scale='Oranges',
            text='mortality_rate'
        )
        fig_mortalidade.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_mortalidade.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            margin=dict(l=150)
        )
        fig_mortalidade = aplicar_layout_padrao(fig_mortalidade, altura=500)
        
        # 4. Casos per Capita por Estado
        fig_per_capita = px.bar(
            df_estados.nlargest(15, 'cases_per_capita'),
            x='cases_per_capita',
            y='state_name',
            orientation='h',
            title='',
            labels={'cases_per_capita': 'Casos por 100k hab.', 'state_name': ''},
            color='cases_per_capita',
            color_continuous_scale='Purples',
            text='cases_per_capita'
        )
        fig_per_capita.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_per_capita.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            margin=dict(l=150)
        )
        fig_per_capita = aplicar_layout_padrao(fig_per_capita, altura=500)
        
        # 5. Casos por Região
        df_regiao = df_estados.groupby('region').agg({
            'last_available_confirmed': 'sum',
            'last_available_deaths': 'sum',
            'population': 'sum'
        }).reset_index()
        
        fig_regiao = px.bar(
            df_regiao,
            x='region',
            y='last_available_confirmed',
            text='last_available_confirmed',
            labels={'region': 'Região', 'last_available_confirmed': 'Casos Confirmados'},
            color='region',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_regiao.update_traces(texttemplate='%{text:,}', textposition='auto')
        fig_regiao.update_layout(showlegend=False)
        fig_regiao = aplicar_layout_padrao(fig_regiao, altura=400)
        
        # 6. Densidade Populacional vs Casos
        fig_densidade = px.scatter(
            df_estados,
            x='population',
            y='last_available_confirmed',
            size='last_available_deaths',
            color='region',
            hover_name='state_name',
            title='',
            labels={
                'population': 'População',
                'last_available_confirmed': 'Casos Confirmados',
                'region': 'Região'
            }
        )
        fig_densidade = aplicar_layout_padrao(fig_densidade, altura=400)
        
        # 7. HeatMap - Casos por Estado
        fig_heatmap = px.treemap(
            df_estados,
            path=['region', 'state_name'],
            values='last_available_confirmed',
            color='mortality_rate',
            color_continuous_scale='RdYlBu_r',
            title='',
            labels={'mortality_rate': 'Taxa Mortalidade (%)'}
        )
        fig_heatmap = aplicar_layout_padrao(fig_heatmap, altura=500)
        
        # 8. Impacto Relativo
        df_estados['impacto_score'] = (
            df_estados['affected_population_pct'] * 0.4 +
            df_estados['mortality_rate'] * 0.3 +
            df_estados['cases_per_capita'] / 1000 * 0.3
        ).round(2)
        
        fig_impacto = px.bar(
            df_estados.nlargest(10, 'impacto_score'),
            x='impacto_score',  # Score no eixo X
            y='state',          # Estado no eixo Y
            orientation='h',    # Barras horizontais
            title='',
            labels={'impacto_score': 'Score de Impacto', 'state': ''},
            color='impacto_score',
            color_continuous_scale='Reds'
        )
        fig_impacto.update_layout(
            margin=dict(l=40, r=40, t=40, b=40)
        )
        fig_impacto = aplicar_layout_padrao(fig_impacto, altura=500)
        
        # 9. Rankings de Impacto (COM CORREÇÃO DE NOMES)
        estados_maior_impacto = df_estados.nlargest(5, 'impacto_score').copy()
        estados_menor_impacto = df_estados.nsmallest(5, 'impacto_score').copy()
        
        # Mapeamento de correção de nomes (caso necessário)
        corretor_nomes = {
            'Pontuação pernambucana': 'Pernambuco',
            'Pontuação do Maranhão': 'Maranhão',
            'Pontuação do Pará': 'Pará',
            'Pontuação de Alagoas': 'Alagoas',
            'Pontuação baiana': 'Bahia'
        }
        
        # DEBUG: Verificar os dados antes da correção
        print("DEBUG - Estados com menor impacto (ANTES da correção):")
        for idx, row in estados_menor_impacto.iterrows():
            print(f"  {idx}: '{row['state_name']}' | Score: {row['impacto_score']:.2f}")
        
        # RECONSTRUÇÃO MANUAL - MAIOR IMPACTO
        ranking_maior_list = []
        for idx, row in estados_maior_impacto.iterrows():
            estado_nome_original = str(row.get('state_name', 'Estado Desconhecido')).strip()
            estado_nome = corretor_nomes.get(estado_nome_original, estado_nome_original)
            score = float(row.get('impacto_score', 0))
            mortalidade = float(row.get('mortality_rate', 0))
            pop_afetada = float(row.get('affected_population_pct', 0))
            
            ranking_maior_list.append(
                html.Li([
                    html.Strong(estado_nome, className="text-danger"),
                    html.Br(),
                    html.Small(
                        f"Score: {score:.2f} | Mortalidade: {mortalidade:.1f}% | Pop. Afetada: {pop_afetada:.2f}%",
                        className="text-muted"
                    )
                ], className="mb-2")
            )
        
        ranking_maior = html.Div([html.Ol(ranking_maior_list)])
        
        # SOLUÇÃO ALTERNATIVA: SUBSTITUIÇÃO DIRETA
        ranking_menor_list = []
        for idx, row in estados_menor_impacto.iterrows():
            estado = row['state']
            score = float(row.get('impacto_score', 0))
            mortalidade = float(row.get('mortality_rate', 0))
            pop_afetada = float(row.get('affected_population_pct', 0))
            
            # Mapeamento direto por UF
            estado_nome = {
                'MA': 'Maranhão',
                'PA': 'Pará',
                'AL': 'Alagoas',
                'PE': 'Pernambuco',
                'BA': 'Bahia'
            }.get(estado, f"Estado {estado}")
            
            ranking_menor_list.append(
                html.Li([
                    html.Strong(f"{estado_nome}", className="text-success"),
                    html.Br(),
                    html.Small(
                        f"Score: {score:.2f} | Mortalidade: {mortalidade:.1f}% | Pop. Afetada: {pop_afetada:.2f}%",
                        className="text-muted"
                    )
                ], className="mb-2")
            )
        
        ranking_menor = html.Div([html.Ol(ranking_menor_list)])
        
        print("✅ Todos os gráficos e análises criados com sucesso")
        
        # RETORNO CORRIGIDO
        return (
            f"{total_casos:,}",
            f"{total_obitos:,}",
            f"{taxa_mortalidade:.2f}%",  # ✅ Adicionado %
            f"{populacao_afetada:.2f}%",  # ✅ Adicionado %
            f"{casos_novos:,}",
            f"{obitos_novos:,}",
            f"{incidencia:,.0f}",
            ultima_data,
            fig_top_casos,
            fig_top_obitos,
            fig_mortalidade,
            fig_per_capita,
            fig_regiao,
            fig_densidade,
            fig_heatmap,
            fig_impacto,
            ranking_maior,
            ranking_menor
        )
        
    except Exception as e:
        print(f"❌ Erro no callback: {e}")
        import traceback
        traceback.print_exc()
        
        empty_fig = {'data': [], 'layout': {'title': 'Erro ao carregar dados'}}
        empty_content = html.P("Erro ao carregar dados")
        return ["Erro"] * 8 + [empty_fig] * 10 + [empty_content, empty_content]
