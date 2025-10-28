# Arquivo principal da aplicação

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import sys
import os

# Adicionar o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Inicializar a aplicação Dash
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

# Configurar o servidor para o Cloud Run
server = app.server

# Layout principal
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Painel COVID-19", className="text-center text-primary mb-4"),
            html.P("Análise de dados da COVID-19 no Brasil e no mundo", 
                  className="text-center text-muted mb-4")
        ])
    ]),
    
    # Navegação
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Brasil", href="/brasil", id="nav-brasil")),
                dbc.NavItem(dbc.NavLink("Comparação", href="/comparacao", id="nav-comparacao")),
            ], pills=True, justified=True)
        ])
    ], className="mb-4"),
    
    # Conteúdo dinâmico
    html.Div(id="page-content"),
    
    # URL routing
    dcc.Location(id="url", refresh=False)
    
], fluid=True)

# Callback de navegação
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    print(f"Navegação para: {pathname}")
    
    try:
        if pathname == '/brasil' or pathname == '/':
            # Importar e criar o layout do dashboard Brasil
            from src.components.brasil_dashboard import create_brasil_dashboard
            layout = create_brasil_dashboard()
            print("Dashboard Brasil carregado")
            return layout
        elif pathname == '/comparacao':
            from src.components.comparison_dashboard import create_comparison_dashboard
            layout = create_comparison_dashboard()
            print("Dashboard Comparação carregado")
            return layout
        else:
            return html.Div([
                html.H3('Página não encontrada'),
                html.P('A página solicitada não existe.')
            ])
    except ImportError as ie:
        print(f"Erro de importação: {ie}")
        return html.Div([
            html.H3('Erro ao carregar página'),
            html.P(f'Erro de importação: {str(ie)}'),
            html.P('Verifique se todos os arquivos estão no local correto.')
        ])
    except Exception as e:
        print(f" Erro geral: {e}")
        return html.Div([
            html.H3('Erro ao carregar página'),
            html.P(f'Erro: {str(e)}'),
            html.P('Verifique se todas as dependências estão instaladas.')
        ])

# Importar os callbacks APÓS definir o layout
try:
    print("Registrando callbacks...")
    # Isso vai registrar os callbacks dos dashboards
    import src.components.brasil_dashboard
    import src.components.comparison_dashboard
    print("Callbacks registrados com sucesso")
except Exception as e:
    print(f" Erro ao registrar callbacks: {e}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print("="*50)
    print("INICIANDO DASHBOARD COVID-19")
    print("="*50)
    print(f" Acesse: http://{host}:{port}")
    print("="*50)
    app.run_server(debug=False, host=host, port=port)
