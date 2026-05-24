# Dashboard COVID-19 Brasil

[![CI](https://github.com/Lucasfonseca2002/Dashboard-COVID-19/actions/workflows/ci.yml/badge.svg)](https://github.com/Lucasfonseca2002/Dashboard-COVID-19/actions/workflows/ci.yml)

Um dashboard interativo para análise de dados da COVID-19 no Brasil, desenvolvido com Streamlit e Python.

## 🌐 Acesso Online

**🚀 Dashboard em Produção:** [https://dash-covid-19.streamlit.app/](https://dash-covid-19.streamlit.app/)

> Acesse o dashboard diretamente no seu navegador - sem necessidade de instalação!

## 📋 Descrição

Este projeto apresenta um dashboard interativo completo para visualização e análise de dados da COVID-19 no Brasil. Com uma interface moderna e intuitiva, oferece múltiplas visualizações, análises estatísticas avançadas e mapas interativos para acompanhamento da pandemia.

## ✨ Funcionalidades

### 📊 Visão Geral
- Painel com indicadores principais (casos totais, óbitos, recuperados)
- Gráficos de evolução temporal
- Séries históricas personalizáveis

### 🗺️ Visualizações Geográficas
- Mapa interativo do Brasil com dados por estado
- Visualização de densidade de casos
- Comparação regional

### 📈 Análises Avançadas
- **Médias Móveis**: Suavização de dados com médias móveis de 7 dias
- **Análises Per Capita**: Normalização por 100k habitantes
- **Análise Regional**: Comparação entre regiões do Brasil
- **Tendências**: Identificação de padrões e tendências

### 🔍 Recursos Interativos
- Filtros por estado e período
- Gráficos dinâmicos e responsivos
- Download de dados
- Interface responsiva para desktop e mobile

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

- **Python 3.9+** - Linguagem de programação
- **Streamlit** - Framework para criação do dashboard
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas e gráficos
- **Folium** - Mapas interativos
- **Requests** - Requisições HTTP para APIs
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes do Python)

### Passos para instalação

1. Clone o repositório:
```bash
git clone https://github.com/Lucasfonseca2002/Dashboard-COVID-19.git
cd Dashboard-COVID-19
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave API do Brasil.IO
# Obtenha sua chave em: https://brasil.io/auth/tokens/
```

6. Execute a aplicação:
```bash
streamlit run streamlit_app.py
```

7. Acesse o dashboard em seu navegador:
```
http://localhost:8501
```

## ☁️ Deploy no Streamlit Cloud

### Opção Recomendada para Publicação

O Streamlit Cloud é a forma mais simples e gratuita de publicar sua aplicação:

1. **Faça push do código para o GitHub**
2. **Acesse**: [share.streamlit.io](https://share.streamlit.io)
3. **Conecte seu repositório GitHub**
4. **Configure**:
   - Repository: seu repositório
   - Branch: main
   - Main file: `streamlit_app.py`
5. **Deploy**: A aplicação será publicada automaticamente

### Vantagens do Streamlit Cloud:
- ✅ **Gratuito** para aplicações públicas
- ✅ **Deploy automático** a cada push
- ✅ **SSL/HTTPS** incluído
- ✅ **Fácil configuração** de secrets/variáveis
- ✅ **Monitoramento** integrado

📖 **Guia completo**: Veja o arquivo [`docs/streamlit_cloud_deploy.md`](docs/streamlit_cloud_deploy.md) para instruções detalhadas.

## 🐳 Deploy no Google Cloud Run

1. Instale e configure o Google Cloud SDK e Docker Desktop
2. Crie um projeto no Google Cloud e associe uma conta de faturamento
3. Ative as APIs: Cloud Run Admin API e Google Container Registry API
4. Faça o build e push da imagem Docker para o Container Registry
5. Crie o serviço no Cloud Run, selecione a imagem enviada e configure as variáveis de ambiente (ex: `BRASIL_IO_API_KEY`)
6. Permita invocações não autenticadas para acesso público
7. Acesse o dashboard pela URL fornecida pelo Cloud Run:

**Dashboard online:**
[https://dashboard-covid19-517319361202.southamerica-east1.run.app](https://dashboard-covid19-517319361202.southamerica-east1.run.app)

## 📁 Estrutura do Projeto

```
Dashboard-COVID-19/
├── streamlit_app.py           # Arquivo principal da aplicação Streamlit
├── requirements.txt           # Dependências do projeto
├── Dockerfile                 # Configuração do container Docker
├── .dockerignore              # Arquivos ignorados no build
├── .env.example               # Template de variáveis de ambiente
├── .gitignore                 # Arquivos ignorados pelo Git
├── src/                       # Código fonte
│   ├── components/            # Componentes do dashboard
│   │   ├── advanced_analytics.py    # Análises avançadas
│   │   └── common_components.py     # Componentes reutilizáveis
│   ├── data/                  # Módulos de dados
│   │   ├── api_client.py      # Cliente para APIs externas
│   │   └── data_processor.py  # Processamento de dados
│   └── utils/                 # Funções utilitárias
│       ├── constants.py       # Constantes do projeto
│       └── helpers.py         # Funções auxiliares
├── assets/                    # Arquivos estáticos (CSS, imagens)
├── tests/                     # Testes automatizados
└── docs/                      # Documentação adicional
```

## 📦 Boas Práticas - Arquivos no Repositório

### ✅ Inclua no repositório:
- Todo o código fonte (`streamlit_app.py`, `src/`, `assets/`, `tests/`, `docs/`)
- `requirements.txt` - Dependências do projeto
- `Dockerfile` e `.dockerignore` - Configuração Docker
- `.env.example` - Template de variáveis de ambiente
- `.gitignore` - Arquivos a serem ignorados
- `README.md` - Documentação

### ❌ Não inclua no repositório:
- `.env` - Contém chaves de API e informações sensíveis
- `.venv/`, `venv/`, `ENV/` - Ambientes virtuais Python
- `__pycache__/`, `*.pyc`, `*.pyo` - Cache do Python
- `.DS_Store`, `Thumbs.db` - Arquivos do sistema operacional
- Dados pessoais ou sensíveis

### 🔐 Segurança:
- **Nunca** commite chaves de API ou tokens
- Use `.env.example` como template (sem valores reais)
- Configure secrets no Streamlit Cloud para produção
- Regenere chaves de API se forem expostas acidentalmente

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
