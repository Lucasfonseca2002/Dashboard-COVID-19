# Melhorias de Infraestrutura — requirements.txt, Dockerfile e docker-compose.yml

## O que foi modificado / criado

| Arquivo | Ação | Descrição |
|---|---|---|
| `requirements.txt` | Modificado | Versões travadas com `==` |
| `Dockerfile` | Modificado | Usuário não-root, HEALTHCHECK, LABEL |
| `docker-compose.yml` | Criado | Orquestração para desenvolvimento local |

---

## 1. requirements.txt — Travamento de versões

### Antes
```
streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
```

### Depois
```
streamlit==1.45.1
plotly==6.1.2
pandas==2.2.3
```

### Por que travar versões?

Com `>=`, o pip instala **a versão mais recente disponível** no momento do `pip install`. Isso significa que dois builds feitos em datas diferentes podem resultar em ambientes diferentes — o que é chamado de **build não-reproduzível**.

Com `==`, todo build (local, CI, produção, container Docker) instala exatamente o mesmo conjunto de pacotes. Isso é uma prática fundamental de **dependency pinning** e segue o princípio de **builds determinísticos**.

| Aspecto | `>=` | `==` |
|---|---|---|
| Reprodutibilidade | ❌ Não garantida | ✅ Garantida |
| Segurança | ❌ Pode instalar versão com bug | ✅ Versão auditada |
| Manutenção | Fácil atualizar | Requer atualização explícita |

> **Nota:** As versões foram fixadas nas mais recentes estáveis (maio/2025), pois as dependências não estavam instaladas no ambiente local. Para projetos em produção, o processo correto é: instalar com `>=`, executar `pip freeze > requirements.txt`, testar, commitar.

### Separação dev vs. produção

`pytest` e `pytest-mock` foram mantidos no mesmo arquivo, mas com comentário indicando que são dependências de teste. Para projetos maiores, recomenda-se separar em `requirements-dev.txt`.

---

## 2. Dockerfile — Segurança e observabilidade

### Usuário não-root

```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
# ...instalação de dependências como root...
RUN chown -R appuser:appuser /app
USER appuser
```

**Por que isso importa?**

Por padrão, processos em containers Docker rodam como `root`. Se um atacante explorar uma vulnerabilidade na aplicação (ex: uma biblioteca com CVE), ele terá privilégios de root dentro do container — o que pode facilitar escapes de container e comprometimento do host.

Rodar como usuário não-privilegiado (`appuser`) limita o **raio de blast** de qualquer ataque. Isso segue o princípio de **menor privilégio** (Principle of Least Privilege — PoLP).

**Ordem das instruções:**
1. `useradd` é executado **antes** do `COPY` — o usuário precisa existir antes de `chown`
2. `pip install` é executado como **root** (necessário para instalar em `/usr/local/lib`)
3. `chown` transfere a propriedade dos arquivos
4. `USER appuser` troca de contexto — a partir daqui todos os comandos rodam como appuser

### LABEL — Metadados OCI

```dockerfile
LABEL maintainer="..." \
      version="1.0.0" \
      description="..." \
      org.opencontainers.image.title="..." \
      org.opencontainers.image.source="..." \
      org.opencontainers.image.licenses="MIT"
```

Labels seguem o padrão **OCI Image Spec** (`org.opencontainers.image.*`), que é reconhecido por registries como Docker Hub, GitHub Container Registry e ferramentas de auditoria de segurança. Permitem:
- Rastrear qual versão do código gerou uma imagem
- Filtrar imagens por metadados (`docker images --filter label=version=1.0.0`)
- Auditoria de licenças e conformidade

### HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" \
    || exit 1
```

| Parâmetro | Valor | Significado |
|---|---|---|
| `--interval` | 30s | Frequência das verificações |
| `--timeout` | 10s | Tempo máximo para o health check responder |
| `--start-period` | 30s | Tempo de carência após o start (Streamlit demora para iniciar) |
| `--retries` | 3 | Tentativas antes de marcar como `unhealthy` |

O endpoint `/_stcore/health` é nativo do Streamlit (desde v1.12) e retorna HTTP 200 quando o servidor está pronto para receber conexões.

Usamos `urllib.request` em vez de `curl` ou `wget` porque a imagem `python:3.9-slim` já tem Python — sem precisar instalar ferramentas extras, o que mantém a imagem menor.

**Impacto no docker-compose e orquestradores:**
- `docker compose` aguarda o container ficar `healthy` antes de iniciar dependências
- Kubernetes usa a mesma lógica em `livenessProbe` / `readinessProbe`

### Variáveis ENV consolidadas

```dockerfile
ENV PORT=8501 \
    HOST=0.0.0.0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

- `PYTHONDONTWRITEBYTECODE=1` — impede criação de arquivos `.pyc` (menos lixo no container)
- `PYTHONUNBUFFERED=1` — força o stdout/stderr a não fazer buffer, garantindo que logs apareçam imediatamente (essencial para observabilidade em produção)

---

## 3. docker-compose.yml — Desenvolvimento local

```yaml
services:
  dashboard:
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - .env
    environment:
      - BRASIL_IO_API_KEY=${BRASIL_IO_API_KEY}
    volumes:
      - .:/app
      - /app/__pycache__
```

### Como funciona o carregamento de variáveis

```
.env (arquivo local, NÃO commitado)
  └─ env_file: .env      → carrega todas as variáveis do arquivo
  └─ environment:        → passa variável específica para o container
       BRASIL_IO_API_KEY=${BRASIL_IO_API_KEY}   (interpolação do docker-compose)
```

A dupla declaração (`env_file` + `environment`) é uma escolha explícita: `env_file` carrega o `.env` no escopo do compose, e `environment` repassa explicitamente para o container apenas as variáveis necessárias. Isso torna visível no arquivo quais variáveis a aplicação consome.

### Volume para hot-reload

```yaml
volumes:
  - .:/app                # Código local montado dentro do container
  - /app/__pycache__      # Volume anônimo: evita que __pycache__ do container sobrescreva o local
```

O volume anônimo `/app/__pycache__` é um padrão comum para evitar conflitos de bytecode entre o sistema operacional do host (Windows/Mac) e o Linux do container.

### Segurança do .env

O arquivo `.env` já está no `.gitignore`. O `.env.example` documenta quais variáveis são necessárias sem expor valores reais. Esse é o padrão estabelecido pela comunidade para configuração via ambiente (12-Factor App — fator III: Config).

---

## Como usar

### Desenvolvimento local com Docker

```bash
# 1. Copiar e preencher o .env
cp .env.example .env
# editar .env com seu BRASIL_IO_API_KEY

# 2. Subir o container
docker compose up --build

# 3. Acessar o dashboard
# http://localhost:8501
```

### Verificar saúde do container

```bash
docker inspect --format='{{.State.Health.Status}}' covid19-dashboard
# → healthy
```

### Build isolado (sem compose)

```bash
docker build -t covid19-dashboard:1.0.0 .
docker run -p 8501:8501 --env-file .env covid19-dashboard:1.0.0
```

---

## Boas práticas de engenharia aplicadas

| Prática | Onde | Detalhe |
|---|---|---|
| **Builds reproduzíveis** | `requirements.txt` | Versões fixas com `==` eliminam não-determinismo |
| **Menor privilégio** | `Dockerfile` | `appuser` não-root reduz superfície de ataque |
| **Observabilidade** | `Dockerfile` | `HEALTHCHECK` + `PYTHONUNBUFFERED` garantem visibilidade do estado |
| **Metadados OCI** | `Dockerfile` | Labels padrão permitem rastreabilidade de imagens |
| **12-Factor App** | `docker-compose.yml` | Configuração via ambiente, nunca hardcoded |
| **Segredos fora do repositório** | `.env` / `.gitignore` | Credenciais nunca commitadas |
| **Documentação de contrato** | `.env.example` | Documenta variáveis sem expor valores |

## Pontos de atenção / melhorias futuras

- **`requirements-dev.txt`** — Para escalar, separar dependências de teste (`pytest`, `pytest-mock`) em arquivo dedicado e não instalá-las na imagem de produção.
- **Multi-stage build** — Uma imagem Docker ainda menor seria possível com multi-stage: instalar dependências em um estágio e copiar apenas o necessário para a imagem final.
- **Renovação de versões** — Com versões fixas, é necessário um processo periódico de atualização (ex: Dependabot, pip-compile). Sem isso, vulnerabilidades conhecidas nas versões travadas não serão corrigidas automaticamente.
