# Dashboard-COVID-19

Um dashboard interativo para análise de dados da COVID-19 no Brasil e no mundo, desenvolvido com Dash e Python.

## 📊 Sobre o Projeto

Este projeto apresenta um dashboard interativo que permite visualizar e analisar dados da COVID-19, com foco especial no Brasil. O dashboard oferece diferentes visualizações e análises comparativas, permitindo uma compreensão mais profunda da evolução da pandemia.

**Dashboard online:**
[https://dashboard-covid19-517319361202.southamerica-east1.run.app](https://dashboard-covid19-517319361202.southamerica-east1.run.app)

## ✨ Funcionalidades

- Visualização de dados da COVID-19 no Brasil
- Análise comparativa entre diferentes países
- Gráficos interativos e atualizados
- Interface responsiva e intuitiva
- Navegação entre diferentes visualizações

## 🌐 APIs Utilizadas

O projeto utiliza duas APIs principais para obtenção dos dados:

1. **API Brasil.io**
   - URL Base: `https://api.brasil.io/v1/dataset/covid19`
   - Fornece dados detalhados da COVID-19 no Brasil
   - Requer chave de API (Token)
   - Dados por estado e município
   - Métricas: casos confirmados, óbitos, recuperados

2. **API Disease.sh**
   - URL Base: `https://disease.sh/v3/covid-19`
   - Fornece dados globais da COVID-19
   - Não requer autenticação
   - Dados por país e continente
   - Métricas: casos, mortes, recuperados, testes

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Dash
- Plotly
- Pandas
- Dash Bootstrap Components
- Requests
- Python-dotenv
- Gunicorn
- Docker

## 🚀 Como Executar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/dashboard-covid19.git
cd dashboard-covid19
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da API Brasil.io:
   ```
   BRASIL_IO_API_KEY=sua_chave_aqui
   ```

5. Execute a aplicação:
```bash
python app.py
```

6. Acesse o dashboard em seu navegador:
```
http://127.0.0.1:8050
```

## ☁️ Deploy no Google Cloud Run

1. Instale e configure o Google Cloud SDK e Docker Desktop
2. Crie um projeto no Google Cloud e associe uma conta de faturamento
3. Ative as APIs: Cloud Run Admin API e Google Container Registry API
4. Faça o build e push da imagem Docker para o Container Registry
5. Crie o serviço no Cloud Run, selecione a imagem enviada e configure as variáveis de ambiente (ex: `BRASIL_IO_API_KEY`)
6. Permita invocações não autenticadas para acesso público
7. Acesse o dashboard pela URL fornecida pelo Cloud Run:

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
