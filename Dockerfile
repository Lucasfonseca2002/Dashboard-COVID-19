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

# Expor a porta que o Dash usa
EXPOSE 8050

# Configurar variáveis de ambiente
ENV PORT=8050
ENV HOST=0.0.0.0

# Comando para executar a aplicação
CMD gunicorn app:server --bind 0.0.0.0:8080