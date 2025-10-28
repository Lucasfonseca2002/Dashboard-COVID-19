# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Expor a porta que o Streamlit usa
EXPOSE 8501

# Configurar variáveis de ambiente
ENV PORT=8501
ENV HOST=0.0.0.0

# Comando para executar a aplicação
CMD streamlit run streamlit_app.py --server.port=$PORT --server.address=$HOST --server.headless=true