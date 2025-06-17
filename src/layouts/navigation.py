# Navegação entre dashboards

from dash import callback, Input, Output, html
from src.components.brasil_dashboard import create_brasil_dashboard
from src.components.comparison_dashboard import create_comparison_dashboard

def register_navigation_callbacks(app):
    """Registra os callbacks de navegação"""
    
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/brasil' or pathname == '/':
            return create_brasil_dashboard()
        elif pathname == '/comparacao':
            return create_comparison_dashboard()
        else:
            return html.Div([
                html.H3('Página não encontrada'),
                html.P('A página solicitada não existe.')
            ])