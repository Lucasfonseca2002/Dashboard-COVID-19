# Constantes do projeto

"""Constantes utilizadas no projeto"""

# URLs das APIs
BRASIL_IO_API_URL = "https://api.brasil.io/v1/dataset/covid19"
WORLD_COVID_API_URL = "https://disease.sh/v3/covid-19"

# Configurações de atualização
UPDATE_INTERVAL = 300000  # 5 minutos em millisegundos

# Cores para gráficos
COLORS = {
    'primary': '#007bff',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'success': '#28a745'
}

# Estados brasileiros
ESTADOS_BRASIL = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
    'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
    'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]
