# 📚 Organiza Aí Estudos

Aplicação web para organização de rotina de estudos: cadastro de horários livres, disciplinas, e geração automática de cronograma semanal com exportação em PDF.

---

## ✨ Funcionalidades

- 🔐 Login e cadastro de usuário
- ⏰ Cadastro de horários livres por dia da semana
- 📖 Cadastro, edição e remoção de disciplinas
- 🗓️ Geração automática de cronograma semanal
- 📄 Exportação do cronograma em PDF

---

## 🗂️ Estrutura do projeto

```
organiza-ai/
├── app.py                 # Tela de login / cadastro (RF01)
├── auth.py                # Autenticação do usuário (RF01)
├── disciplinas.py         # Regras de disciplinas (RF02)
├── horarios.py             # Regras de horários livres (RF03)
├── cronograma.py          # Geração e exportação do cronograma (RF04, RF05, RF06)
├── database.py            # Acesso ao banco de dados PostgreSQL (RF07)
├── interface.py           # Sidebar de navegação compartilhada
├── pages/
│   ├── inicio.py           # Página inicial / resumo
│   ├── rotina.py           # Página de horários livres
│   ├── disciplinas.py      # Página de disciplinas
│   └── cronograma.py       # Página do cronograma
├── .streamlit/
│   └── secrets.toml        # Credenciais do banco (não vai para o GitHub)
├── requirements.txt
└── .gitignore
```

### Matriz de rastreabilidade

| Requisito | Módulo | Responsabilidade |
|---|---|---|
| RF01 | `auth.py` | Login do usuário → sessão autenticada |
| RF02 | `disciplinas.py` | Cadastro de disciplinas → lista de disciplinas |
| RF03 | `horarios.py` | Cadastro de horários livres → lista por dia |
| RF04 / RF05 | `cronograma.py` | Geração e recálculo do cronograma semanal |
| RF06 | `cronograma.py` | Exportação do cronograma em PDF |
| RF07 | `database.py` | Persistência de todos os dados (PostgreSQL) |

---

## 🚀 Como colocar no ar (GitHub + Render + Streamlit Cloud)

### 1. Banco de dados (Render)
1. Crie uma conta em [render.com](https://render.com)
2. **New → PostgreSQL** → plano **Free** → **Create Database**
3. Copie a **External Database URL**

### 2. Repositório (GitHub)
```bash
git init
git add .
git commit -m "Organiza Aí Estudos"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/organiza-ai-estudos.git
git push -u origin main
```
> O arquivo `.streamlit/secrets.toml` **não é enviado** ao GitHub (está no `.gitignore`), pois contém a senha do banco.

### 3. Deploy (Streamlit Cloud)
1. Acesse [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Selecione o repositório, branch `main`, arquivo principal `app.py`
3. Em **Advanced settings → Secrets**, cole:
```toml
DATABASE_URL = "postgresql://usuario:senha@host/banco"
```
4. Clique em **Deploy!**

---

## 💻 Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

> É necessário ter o arquivo `.streamlit/secrets.toml` com a `DATABASE_URL` preenchida.

---

## 📦 Dependências

| Pacote | Uso |
|---|---|
| `streamlit` | Interface web |
| `psycopg2-binary` | Conexão com PostgreSQL |
| `fpdf2` | Geração do PDF do cronograma |
