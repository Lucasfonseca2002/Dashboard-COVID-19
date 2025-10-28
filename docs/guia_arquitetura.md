# Guia detalhado da arquitetura do projeto

Este documento explica, passo a passo, como o projeto funciona, o papel de cada pasta e de cada arquivo relevante, e sugere uma ordem de leitura.

## Objetivo do projeto
- Coletar dados de COVID-19 de APIs públicas (Brasil e mundo).
- Processar e calcular métricas com `pandas`.
- Visualizar análises interativas com `Streamlit` (`streamlit_app.py`).

## Ordem sugerida de leitura
1. `src/utils/constants.py`
2. `src/data/api_client.py`
3. `streamlit_app.py` e `src/components/advanced_analytics.py`
4. `src/components/common_components.py`
5. `tests/` (diagnósticos e exemplos)
6. `.streamlit/config.toml` e `.streamlit/secrets.toml`
7. `Dockerfile`, `requirements.txt` e `README.md`

## Pastas e arquivos (o que cada um faz)

### Raiz do projeto
- `streamlit_app.py`
  - App Streamlit com páginas: Brasil, Análises Avançadas, Comparação Mundial.
  - Usa `@st.cache_data` para cachear chamadas ao cliente de API.
  - Renderiza métricas (cards e `st.metric`) e gráficos com Plotly.
- `requirements.txt`
  - Dependências: `streamlit`, `plotly`, `pandas`, `requests`, `python-dotenv`, `folium`, `streamlit-folium`, etc.
- `Dockerfile`
  - Instala dependências, copia o código e inicia com `streamlit run streamlit_app.py`.
  - Exposição de porta 8501 e variáveis (`PORT`, `HOST`).
- `.env`
  - Contém `BRASIL_IO_API_KEY`. Não versionar publicamente.
- `assets/`
  - `style.css`, `favicon.ico`: estáticos para UI.
- `docs/`
  - Documentação (este guia e outros materiais, ex.: `comparison_dashboard.md`).

### `src/` (código fonte)
- `src/utils/constants.py`
  - URLs das APIs (`BRASIL_IO_API_URL`, `WORLD_COVID_API_URL`).
  - `UPDATE_INTERVAL`, paleta de `COLORS`, `ESTADOS_BRASIL`.
- `src/utils/helpers.py`
  - Placeholder para utilitários; pode receber funções de formatação/cache futuramente.
- `src/data/api_client.py`
  - Classe `COVID19APIClient` encapsula chamadas às APIs.
  - Métodos:
    - `get_brasil_data()`: dados atuais por estado (Brasil.io, requer token).
    - `get_brasil_historical_data(limit=None)`: histórico; converte `date` e ordena por `state/date`.
    - `get_brasil_time_series(state=None, days=30)`: recorte temporal por estado/dias.
    - `get_world_top_countries(limit=10)`: top países (API `disease.sh`, sem autenticação; exclui Brasil).
    - `get_world_countries_data(countries)`: países específicos.
    - `calculate_moving_averages(df, window=7)`: médias móveis para `new_confirmed` e `new_deaths` por estado.
- `src/data/data_processor.py`
  - Atualmente vazio; planejado para centralizar transformações/limpezas adicionais.
- `src/components/common_components.py`
  - Funções auxiliares de visualização para Streamlit (ex.: `criar_card_estatistica`, `criar_ranking_lista`, `criar_header`).
- `src/components/advanced_analytics.py`
  - Funções usadas pelo app Streamlit para análises aprofundadas: séries temporais, médias móveis, per capita, regional (inclui mapas `folium`).

### `tests/` (validação e exemplos)
- `test_app_simple.py`
  - Verifica imports principais (Dash, API client, layouts) e criação do cliente.
- `test_components.py`
  - Testa a criação dos layouts de Brasil e Comparação.
- `test_imports.py`
  - Mini app de teste com navegação e callback básico.
- `teste_dashboard_brazil.py`
  - Dashboard simplificado com cards e um gráfico; útil para smoke test.
- `teste_simples_callback.py`
  - Exemplo de callback com botão e `Interval`.
- `test_dashboard_data.py`
  - Exercita `COVID19APIClient` para dados por estado/históricos e imprime métricas.
- `debug_api.py`
  - Diagnóstico detalhado de `.env`, `disease.sh` e Brasil.io (status, colunas, erros comuns).

### `.streamlit/` (configuração do Streamlit)
- `config.toml`
  - Tema, porta (`server.port=8501`), cache e flags de cliente/servidor.
- `secrets.toml`
  - Local de configuração de segredos quando publicado no Streamlit Cloud.

## Fluxo de dados (de ponta a ponta)
- `requests` → baixa JSON das APIs definidas em `constants`.
- `COVID19APIClient` → transforma em `pandas.DataFrame`, ordena e calcula séries/médias.
- Visualização:
  - `Streamlit`: `streamlit_app.py` chama funções de `advanced_analytics.py` e `common_components.py` e exibe com `st.plotly_chart`.

## Como executar e testar
- Ambiente:
  - `python -m venv .venv` e ativar.
  - `pip install -r requirements.txt`.
  - Criar `.env` com `BRASIL_IO_API_KEY`.
- Streamlit: `streamlit run streamlit_app.py` (abre em `http://localhost:8501`).
- Testes: `pytest -q` (ou usar scripts em `tests/` para testes manuais).

## Observações e extensões
- Não versionar `.env`/chaves; usar `secrets.toml` em deploy.
- `data_processor.py` e `helpers.py` podem centralizar lógicas de transformação/formatação futuras.
- Ajuste de `@st.cache_data(ttl=...)` conforme a cadência de atualização desejada.