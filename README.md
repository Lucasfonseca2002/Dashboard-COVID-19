# Dashboard COVID-19

Um dashboard interativo para análise de dados da COVID-19 no Brasil e no mundo, desenvolvido com Streamlit e Python.

## 📋 Descrição

Este projeto apresenta um dashboard interativo que permite visualizar e analisar dados da COVID-19, com foco especial no Brasil. O dashboard oferece diferentes visualizações e análises comparativas, permitindo uma compreensão mais profunda da evolução da pandemia.

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

- Python 3.9+
- Streamlit
- Pandas
- Plotly
- Requests
- Folium (para mapas interativos)
- Geopandas
- Python-dotenv

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes do Python)

### Passos para instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/dashboard-covid19.git
cd dashboard-covid19
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute a aplicação:
```bash
streamlit run streamlit_app.py
```

6. Acesse o dashboard em seu navegador:
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
dashboard-covid19/
├── app.py              # Arquivo principal da aplicação
├── requirements.txt    # Dependências do projeto
├── Dockerfile          # Configuração do container
├── .dockerignore       # Arquivos ignorados no build
├── src/                # Código fonte
│   ├── components/     # Componentes do dashboard
│   └── utils/          # Funções utilitárias
├── assets/             # Arquivos estáticos
├── tests/              # Testes automatizados
└── docs/               # Documentação
```

## 📦 Quais arquivos subir para o repositório?

**Inclua no repositório:**
- Todo o código fonte (`app.py`, `src/`, `assets/`, `tests/`, `docs/`)
- `requirements.txt`
- `Dockerfile`
- `.dockerignore`
- `README.md`

**Não inclua no repositório:**
- Arquivo `.env` (contém informações sensíveis, como chaves de API)
- Pastas de ambiente virtual (`.venv/`, `venv/`, `ENV/`)
- Arquivos de cache Python (`__pycache__/`, `*.pyc`)
- Dados sensíveis ou pessoais

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📧 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/dashboard-covid19](https://github.com/seu-usuario/dashboard-covid19)
