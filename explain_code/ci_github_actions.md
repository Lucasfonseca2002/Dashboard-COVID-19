# Pipeline CI com GitHub Actions — Dashboard COVID-19

## O que foi criado / modificado

| Arquivo | Ação | Descrição |
|---|---|---|
| `.github/workflows/ci.yml` | Criado | Pipeline de integração contínua |
| `requirements.txt` | Modificado | Adicionado `pytest-cov` e `ruff` |
| `README.md` | Modificado | Badge de status do CI adicionado |

---

## Anatomia do workflow (`ci.yml`)

```
on: push / pull_request → main
         │
         ▼
   ┌─────────────┐
   │  Job: lint  │  (ruff check)
   └──────┬──────┘
          │ needs: lint (só avança se lint passar)
          ▼
   ┌─────────────────────────────────────┐
   │  Job: test                          │
   │  pytest --cov=src                   │
   │  → term-missing (terminal)          │
   │  → xml (coverage.xml)               │
   │  → html (htmlcov/)                  │
   │  → $GITHUB_STEP_SUMMARY (PR/push)   │
   │  → upload-artifact (htmlcov.zip)    │
   └─────────────────────────────────────┘
```

### Por que dois jobs separados em vez de um?

Separar `lint` de `test` traz vantagens claras:

| Motivo | Explicação |
|---|---|
| **Falha rápida** | Se há erro de sintaxe, o lint falha em ~10s sem esperar os testes |
| **Checks distintos no PR** | GitHub mostra dois status separados — fica imediatamente visível o que falhou |
| **`needs: lint`** | Evita gastar minutos de CI rodando testes com código que já sabemos que está errado |

---

## Cada step explicado

### `actions/checkout@v4`
Baixa o código do repositório para o runner (máquina virtual da GitHub). Sempre a primeira instrução — sem isso, não há código para executar.

### `actions/setup-python@v5` com `cache: "pip"`
```yaml
uses: actions/setup-python@v5
with:
  python-version: "3.9"
  cache: "pip"
```
O `cache: "pip"` armazena o diretório de cache do pip entre execuções. Na prática, evita baixar todos os pacotes do PyPI a cada push — reduz o tempo do job em 30–60 segundos para projetos com muitas dependências.

### `ruff check . --output-format=github`
```bash
ruff check . --output-format=github
```
O flag `--output-format=github` faz o ruff emitir anotações no formato que o GitHub Actions entende:

```
::error file=src/data/api_client.py,line=10,col=5::F401 'os' imported but unused
```

Isso aparece como comentário inline no diff do Pull Request — o desenvolvedor vê exatamente qual linha precisa corrigir sem precisar abrir logs.

### `pytest --cov=src ...`
```bash
pytest tests/ \
  --cov=src \
  --cov-report=term-missing \
  --cov-report=xml:coverage.xml \
  --cov-report=html:htmlcov \
  -v
```

| Flag | Propósito |
|---|---|
| `--cov=src` | Mede cobertura apenas do código em `src/` (exclui testes, scripts) |
| `--cov-report=term-missing` | Exibe no terminal as linhas não cobertas |
| `--cov-report=xml` | Gera `coverage.xml` (padrão para ferramentas como Codecov, SonarCloud) |
| `--cov-report=html` | Gera relatório HTML navegável em `htmlcov/` |
| `-v` | Modo verbose — lista cada teste individualmente no log |

### `$GITHUB_STEP_SUMMARY`
```bash
echo "## Relatório de Cobertura" >> $GITHUB_STEP_SUMMARY
```

Variável especial do GitHub Actions. Tudo que for escrito nela aparece como **resumo da execução** na aba "Summary" do workflow — visível diretamente no GitHub sem precisar abrir logs. É a forma nativa de exibir relatórios em Markdown no CI.

### `upload-artifact@v4`
```yaml
uses: actions/upload-artifact@v4
with:
  name: coverage-report
  path: htmlcov/
  retention-days: 7
```
Compacta e armazena o relatório HTML de cobertura como artefato do workflow por 7 dias. Qualquer pessoa com acesso ao repositório pode baixar e visualizar a cobertura linha a linha no browser — sem configurar serviços externos.

O `if: always()` garante que o upload acontece mesmo quando os testes falham, permitindo análise do que estava ou não coberto no momento da falha.

---

## O badge no README

```markdown
[![CI](https://github.com/Lucasfonseca2002/Dashboard-COVID-19/actions/workflows/ci.yml/badge.svg)](https://github.com/Lucasfonseca2002/Dashboard-COVID-19/actions/workflows/ci.yml)
```

O badge é uma imagem SVG gerada dinamicamente pelo GitHub com o status da última execução do workflow na branch `main`. Estados possíveis:

| Badge | Significado |
|---|---|
| `passing` (verde) | Último CI passou |
| `failing` (vermelho) | Último CI falhou |
| `no status` | Workflow nunca rodou ou foi desativado |

---

## ruff — por que não flake8 ou pylint?

`ruff` é um linter Python escrito em Rust. A comparação prática:

| Ferramenta | Velocidade | Regras cobertas |
|---|---|---|
| flake8 | ~2–5s | PEP8 básico |
| pylint | ~10–30s | Extenso, mas lento |
| **ruff** | **~0.1–0.5s** | flake8 + isort + pyupgrade + bugbear + mais |

Para CI, velocidade importa — menos tempo de espera por feedback significa que desenvolvedores ficam no fluxo.

Por padrão, o ruff usa um conjunto de regras conservador (E, F — equivalente ao flake8). Para customizar, adicione um `ruff.toml` ou seção `[tool.ruff]` no `pyproject.toml`.

---

## Boas práticas de engenharia aplicadas

| Prática | Onde | Detalhe |
|---|---|---|
| **Fail fast** | `needs: lint` | Testes não rodam se o código não passa no lint |
| **Cache de dependências** | `cache: "pip"` | Builds mais rápidos e baratos |
| **Anotações inline** | `--output-format=github` | Erros de lint aparecem diretamente no diff do PR |
| **Cobertura múltipla** | `term-missing + xml + html` | Terminal, integração futura (Codecov) e relatório visual |
| **Artefato com TTL** | `retention-days: 7` | Relatório disponível para debug sem acumular storage |
| **`if: always()`** | Upload e summary | Relatório gerado mesmo com falha — útil para diagnóstico |
| **Versionamento de actions** | `@v4`, `@v5` | Versão fixada evita quebra por atualizações das actions |

---

## Como verificar localmente antes do push

```bash
# Lint
ruff check .

# Corrigir automaticamente o que for seguro
ruff check . --fix

# Testes com cobertura
pytest tests/ --cov=src --cov-report=term-missing -v
```

## Próximas melhorias sugeridas

- **`--cov-fail-under=80`** — reprovar o CI se a cobertura cair abaixo de 80% (gatilho de regressão)
- **Codecov** — integração com `codecov/codecov-action` para histórico de cobertura por PR
- **Matrix de versões** — testar em Python 3.9, 3.10 e 3.11 simultaneamente com `strategy.matrix`
- **`pyproject.toml`** — centralizar configurações do ruff e pytest (linhas por arquivo, regras ignoradas, etc.)
