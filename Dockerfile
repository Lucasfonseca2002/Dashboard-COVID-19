# ── Metadados da imagem ───────────────────────────────────────────────────────
FROM python:3.9-slim

LABEL maintainer="Lucas Fonseca <lucas@lucasfonseca.dev>" \
      version="1.0.0" \
      description="Dashboard interativo de dados da COVID-19 com Streamlit" \
      org.opencontainers.image.title="Dashboard COVID-19" \
      org.opencontainers.image.source="https://github.com/lucasfonseca/Dashboard-COVID-19" \
      org.opencontainers.image.licenses="MIT"

# ── Variáveis de ambiente ─────────────────────────────────────────────────────
ENV PORT=8501 \
    HOST=0.0.0.0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── Criar usuário não-root ────────────────────────────────────────────────────
RUN useradd --create-home --shell /bin/bash appuser

# ── Diretório de trabalho ─────────────────────────────────────────────────────
WORKDIR /app

# ── Instalar dependências (como root, antes de trocar de usuário) ─────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copiar código e ajustar dono dos arquivos ─────────────────────────────────
COPY . .
RUN chown -R appuser:appuser /app

# ── Trocar para usuário não-root ──────────────────────────────────────────────
USER appuser

# ── Porta exposta ─────────────────────────────────────────────────────────────
EXPOSE 8501

# ── Health check ─────────────────────────────────────────────────────────────
# Streamlit expõe /_stcore/health quando o servidor está pronto
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" \
    || exit 1

# ── Comando de inicialização ──────────────────────────────────────────────────
CMD ["sh", "-c", "streamlit run streamlit_app.py \
    --server.port=$PORT \
    --server.address=$HOST \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false"]
