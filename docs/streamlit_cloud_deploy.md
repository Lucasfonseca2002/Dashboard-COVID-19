# Guia de Publicação no Streamlit Cloud

Este guia explica como publicar o Dashboard COVID-19 no Streamlit Cloud.

## 📋 Pré-requisitos

1. **Conta no GitHub**: Seu código deve estar em um repositório público no GitHub
2. **Conta no Streamlit Cloud**: Crie uma conta gratuita em [share.streamlit.io](https://share.streamlit.io)
3. **Repositório preparado**: Certifique-se de que seu repositório contém:
   - `streamlit_app.py` (arquivo principal)
   - `requirements.txt` (dependências)
   - `.streamlit/config.toml` (configurações opcionais)

## 🚀 Passos para Deploy

### 1. Preparar o Repositório

Certifique-se de que seu repositório GitHub contém:

```
Project_dash_covid_19/
├── streamlit_app.py          # Arquivo principal da aplicação
├── requirements.txt          # Dependências do Python
├── .streamlit/
│   └── config.toml          # Configurações do Streamlit
├── src/                     # Código fonte
│   ├── components/
│   ├── data/
│   └── utils/
└── README.md               # Documentação
```

### 2. Verificar requirements.txt

Certifique-se de que o `requirements.txt` contém todas as dependências necessárias:

```txt
streamlit==1.28.1
plotly==5.17.0
pandas==2.1.4
requests==2.31.0
python-dotenv==1.0.0
geopandas==0.14.1
folium==0.15.0
streamlit-folium==0.15.0
```

### 3. Configurar Secrets (se necessário)

Se sua aplicação usa variáveis de ambiente ou chaves de API:

1. No Streamlit Cloud, vá para as configurações da sua app
2. Adicione os secrets necessários na seção "Secrets"
3. Formato TOML:
```toml
# .streamlit/secrets.toml (não commitar este arquivo)
API_KEY = "sua_chave_aqui"
DATABASE_URL = "sua_url_aqui"
```

### 4. Deploy no Streamlit Cloud

1. **Acesse**: [share.streamlit.io](https://share.streamlit.io)
2. **Login**: Faça login com sua conta GitHub
3. **New app**: Clique em "New app"
4. **Configurar**:
   - **Repository**: Selecione seu repositório
   - **Branch**: Geralmente `main` ou `master`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Escolha uma URL personalizada (opcional)

5. **Deploy**: Clique em "Deploy!"

### 5. Monitorar o Deploy

- O Streamlit Cloud irá instalar as dependências automaticamente
- Você pode acompanhar o progresso na tela de deploy
- Se houver erros, eles serão exibidos no log

## 🔧 Configurações Avançadas

### Configuração de Recursos

O Streamlit Cloud oferece recursos limitados na versão gratuita:
- **CPU**: 1 core
- **RAM**: 1 GB
- **Armazenamento**: 1 GB

### Configurações de Performance

No arquivo `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de dependências**:
   - Verifique se todas as dependências estão no `requirements.txt`
   - Use versões específicas das bibliotecas

2. **Timeout durante o deploy**:
   - Reduza o número de dependências
   - Use bibliotecas mais leves quando possível

3. **Erro de memória**:
   - Otimize o carregamento de dados
   - Use cache do Streamlit (`@st.cache_data`)

4. **Problemas de API**:
   - Configure os secrets corretamente
   - Verifique se as APIs externas estão acessíveis

### Logs e Debug

- Acesse os logs da aplicação no painel do Streamlit Cloud
- Use `st.write()` para debug durante o desenvolvimento
- Monitore o uso de recursos na dashboard

## 🔄 Atualizações

### Deploy Automático

- Qualquer push para a branch configurada irá triggerar um novo deploy
- O Streamlit Cloud detecta mudanças automaticamente
- O processo de build leva alguns minutos

### Deploy Manual

- Você pode forçar um redeploy no painel de controle
- Útil quando há problemas de cache ou dependências

## 📊 Monitoramento

### Analytics

O Streamlit Cloud fornece:
- Número de visitantes
- Tempo de uso
- Erros da aplicação
- Uso de recursos

### Limites da Versão Gratuita

- **Apps públicas**: Ilimitadas
- **Apps privadas**: 1 app
- **Recursos**: Limitados
- **Uptime**: Não garantido para apps inativas

## 🔗 Links Úteis

- [Documentação Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Community](https://discuss.streamlit.io/)
- [Exemplos de Apps](https://streamlit.io/gallery)

## 📝 Exemplo de URL Final

Após o deploy, sua aplicação estará disponível em:
```
https://[app-name]-[random-string].streamlit.app
```

Exemplo:
```
https://dashboard-covid19-abc123.streamlit.app
```