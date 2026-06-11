# 📚 Organiza Aí - Estudos

Um aplicativo inteligente para organizar e planejar sua rotina de estudos com Streamlit.

## 🚀 Features

- ✅ **Autenticação de usuários** com hash seguro de senhas
- 📅 **Gerenciamento de horários** semanais disponíveis para estudo
- 📚 **Cadastro de disciplinas** com prioridades e horas semanais
- 🗓️ **Geração automática de cronogramas** de estudo otimizados
- 📄 **Exportação em PDF** do cronograma

## 📋 Requisitos

- Python 3.8+
- PostgreSQL
- Streamlit

## 🔧 Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/anajuassuncao94/organiza-ai-estudos.git
cd organiza-ai-estudos
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure os secrets localmente:
   - Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml`
   - Adicione sua `DATABASE_URL` do PostgreSQL

5. Execute a aplicação:
```bash
streamlit run app.py
```

## 🌐 Deploy no Streamlit Cloud

1. Faça push do repositório para o GitHub
2. Acesse https://streamlit.io/cloud
3. Clique em **"New app"**
4. Configure:
   - **Repository**: `anajuassuncao94/organiza-ai-estudos`
   - **Branch**: `main`
   - **Main file**: `app.py`
   - **URL**: `organizaai-estudos` → `organizaai-estudos.streamlit.app`

5. Adicione os **Secrets** no painel do Streamlit Cloud:
   - Vá em **Settings → Secrets**
   - Adicione: `DATABASE_URL = "sua_url_postgresql"`

## 📁 Estrutura do Projeto

```
.
├── app.py                      # Aplicação principal Streamlit
├── requirements.txt            # Dependências Python
├── .streamlit/
│   ├── config.toml            # Configuração Streamlit
│   └── secrets.toml.example   # Modelo de secrets
├── .gitignore                 # Arquivos ignorados pelo git
└── README.md                  # Este arquivo
```

## 🔐 Segurança

⚠️ **Importante**: Nunca commite `.streamlit/secrets.toml` com credenciais reais!
- Use `.streamlit/secrets.toml.example` como referência
- Configure os secrets diretamente no painel do Streamlit Cloud

## 📝 Licença

MIT

## 👤 Autor

[anajuassuncao94](https://github.com/anajuassuncao94)