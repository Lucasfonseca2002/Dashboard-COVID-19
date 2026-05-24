# Testes Unitários com pytest — Dashboard COVID-19

## O que foi criado

| Arquivo | Tipo | Descrição |
|---|---|---|
| `src/utils/helpers.py` | Implementação | Funções utilitárias puras (`format_number`, `create_metric_card`) |
| `src/data/data_processor.py` | Implementação | Funções de transformação de dados (`calculate_totals`, `calculate_mortality_rate`, `get_top_states`) |
| `tests/test_api_client.py` | Teste | 16 testes para `get_brasil_data()` e `get_world_top_countries()` |
| `tests/test_data_processor.py` | Teste | 16 testes para as funções de processamento de dados |
| `tests/test_helpers.py` | Teste | 18 testes para `format_number()` e `create_metric_card()` |
| `requirements.txt` | Configuração | Adicionado `pytest>=7.4.0` e `pytest-mock>=3.12.0` |

---

## Por que foi estruturado assim

### Funções puras antes de testes

`helpers.py` e `data_processor.py` estavam vazios. Antes de criar qualquer teste, as funções precisavam existir. A decisão de projeto foi:

- **`helpers.py`** recebe funções utilitárias **sem dependência de framework** (sem Streamlit). Isso é importante porque Streamlit exige um contexto de execução especial — funções que chamam `st.metric()` diretamente não podem ser testadas com pytest sem mocks pesados. `create_metric_card` foi desenhada para retornar um `dict` puro, que a camada de apresentação usa para chamar o Streamlit.

- **`data_processor.py`** recebe funções de **transformação de dados** que operam sobre DataFrames do pandas. São stateless (sem estado), recebem entrada e retornam saída, o que as torna 100% testáveis sem mocks.

### Organização dos testes em classes

Cada arquivo de teste usa **classes por função testada** (ex: `TestGetBrasilData`, `TestCalculateTotals`). Isso segue a convenção do pytest e facilita:
- Agrupar testes relacionados
- Usar fixtures compartilhadas dentro da classe via `self`
- Visualizar resultados agrupados no terminal

### Mocking da camada HTTP

Em `test_api_client.py`, as chamadas HTTP são mockadas com `pytest-mock` (extensão do `unittest.mock`). A estratégia foi **mockar `_make_request`** em vez de `requests.get`, porque:

1. `_make_request` já encapsula o retry, timeout e tratamento de erros HTTP
2. Testar `requests.get` diretamente criaria dependência da implementação interna
3. Mockar um método interno do próprio cliente isola o teste do código de rede

```python
mocker.patch.object(client, "_make_request", return_value=mock_response)
```

---

## Como funciona cada módulo

### `format_number(value, decimal_places=0)`

```python
format_number(38_500_000)       # → "38,500,000"
format_number(2.567, decimal_places=2)  # → "2.57"
format_number(None)             # → "N/A"
format_number("texto")          # → "N/A"
```

Usa a mini-linguagem de formatação do Python (`format(float(value), ",.2f")`). O bloco `try/except` garante que valores inválidos nunca causem crash — retornam `"N/A"`.

### `create_metric_card(title, value, ...)`

```python
card = create_metric_card("Total de Casos", 38_500_000, delta="+500", delta_color="inverse")
# → {"title": "Total de Casos", "value": 38500000, "description": "", "delta": "+500", "delta_color": "inverse"}
```

Retorna um dicionário. A camada de apresentação (`common_components.py`) pode usar esse dict para alimentar `st.metric()`. Isso desacopla a lógica de dados da interface gráfica.

### `calculate_totals(df)`

```python
totais = calculate_totals(df_estados)
# → {"total_cases": 10_000_000, "total_deaths": 340_000, "new_cases": 1_000, "new_deaths": 20}
```

Trata `None` e `DataFrame` vazio de forma defensiva — retorna zeros em vez de levantar exceção.

### `calculate_mortality_rate(total_cases, total_deaths)`

```python
calculate_mortality_rate(1_000_000, 25_000)  # → 2.5
calculate_mortality_rate(0, 0)               # → 0.0
```

Divisão protegida: se `total_cases` for 0 ou None, retorna 0.0.

### `get_top_states(df, column, n=5)`

```python
top = get_top_states(df_estados, "last_available_confirmed", n=3)
# → DataFrame com os 3 estados de maior número de casos, ordenado desc.
```

Usa `DataFrame.nlargest()` do pandas, que é mais eficiente que `sort_values().head()` para grandes DataFrames.

---

## Boas práticas de engenharia aplicadas

| Prática | Como foi aplicada |
|---|---|
| **Separação de responsabilidades** | Lógica de dados (`data_processor`), utilitários (`helpers`) e apresentação (`common_components`) em módulos distintos |
| **Funções puras** | `format_number`, `calculate_mortality_rate` e `calculate_totals` não têm efeitos colaterais — recebem entrada, retornam saída |
| **Testabilidade por design** | `create_metric_card` retorna dict em vez de chamar Streamlit diretamente, eliminando a necessidade de mock do framework |
| **Mock no nível certo** | `_make_request` é mockado (não `requests.get`), respeitando o encapsulamento da classe |
| **Tratamento de borda** | Todos os testes incluem casos de `None`, listas/DataFrames vazios e valores inválidos |
| **Fixtures reutilizáveis** | `@pytest.fixture` isola a criação de dados de teste, evitando duplicação |
| **Nomenclatura descritiva** | Nomes de teste em português descrevem o comportamento esperado (ex: `test_filtra_brasil`) |
| **pytest.approx** | Usado em comparações de float para evitar falhas por erro de ponto flutuante |

---

## Como executar

```bash
# Instalar dependências de teste
pip install pytest pytest-mock

# Rodar todos os testes com saída detalhada
pytest tests/ -v

# Rodar apenas um arquivo
pytest tests/test_api_client.py -v

# Rodar com relatório de cobertura (requer pytest-cov)
pip install pytest-cov
pytest tests/ --cov=src --cov-report=term-missing
```

### Saída esperada

```
tests/test_api_client.py::TestGetBrasilData::test_retorna_dataframe_em_sucesso PASSED
tests/test_api_client.py::TestGetBrasilData::test_colunas_presentes PASSED
...
50 passed in 0.XX s
```

---

## Pontos de atenção / melhorias futuras

- **`data_processor.py`** ainda não tem funções para série temporal — conforme o dashboard evoluir, funções como `aggregate_by_date(df)` devem ser adicionadas aqui (e testadas).
- **Cobertura da `_make_request`** — o retry com backoff exponencial não foi testado diretamente. Recomenda-se adicionar testes para os cenários de timeout e rate limit (429) em iteração futura.
- **`test_dashboard_data.py`** — o arquivo existente não é um teste pytest formal (não usa `assert`, é um script de debug). Pode ser refatorado para seguir o mesmo padrão dos novos testes.
