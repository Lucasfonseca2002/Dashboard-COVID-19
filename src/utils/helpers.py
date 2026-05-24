    # Funções auxiliares

def format_number(value, decimal_places=0):
    """Formata um número com separadores de milhar e casas decimais opcionais.

    Parâmetros:
    -----------
    value : int | float | None
        Valor a ser formatado.
    decimal_places : int
        Número de casas decimais (padrão 0).

    Retorna:
    --------
    str
        Número formatado ou "N/A" se o valor for None.
    """
    if value is None:
        return "N/A"
    try:
        fmt = f",.{decimal_places}f"
        return format(float(value), fmt)
    except (TypeError, ValueError):
        return "N/A"


def create_metric_card(title, value, description="", delta=None, delta_color="normal"):
    """Constrói um dicionário com os dados de um card de métrica.

    Não depende do Streamlit — retorna um dict puro que pode ser passado para
    componentes de apresentação ou verificado em testes unitários.

    Parâmetros:
    -----------
    title : str
        Título da métrica.
    value : str | int | float
        Valor principal a ser exibido.
    description : str
        Texto explicativo.
    delta : str | None
        Valor de variação a ser exibido.
    delta_color : str
        Cor do delta ("normal", "inverse", "off").

    Retorna:
    --------
    dict
        Dicionário com as chaves: title, value, description, delta, delta_color.
    """
    return {
        "title": title,
        "value": value,
        "description": description,
        "delta": delta,
        "delta_color": delta_color,
    }
