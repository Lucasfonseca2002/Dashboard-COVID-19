# Layout principal

from dash import dcc, html
import dash_bootstrap_components as dbc

def create_main_layout():
    """Cria o layout principal da aplicação"""
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("Dashboard COVID-19", className="text-center text-primary mb-4"),
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
