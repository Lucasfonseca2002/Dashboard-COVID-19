# Scripts de Diagnóstico

Scripts auxiliares para debug e diagnóstico manual. **Não são testes automatizados** — use `pytest tests/` para os testes reais.

| Script | Descrição |
|---|---|
| `debug_api.py` | Diagnóstico de conectividade com as APIs Brasil.io e Disease.sh |
| `debug_dashboard_data.py` | Validação manual dos dados exibidos no dashboard |
| `debug_map.py` | Teste de dados e dependências necessárias para o mapa interativo |

## Como usar

```bash
# Na raiz do projeto, com o venv ativado:
python scripts/debug_api.py
python scripts/debug_dashboard_data.py
python scripts/debug_map.py
```
