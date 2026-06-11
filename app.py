import streamlit as st
import psycopg2
import hashlib

st.set_page_config(page_title="Organiza Aí Estudos", page_icon="📚", layout="wide")

# Esconde a navegação padrão do Streamlit (pages/)
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

DB_URL = st.secrets["DATABASE_URL"]

def conn():
    return psycopg2.connect(DB_URL)

def q(sql, params=(), fetch=False):
    c = conn(); cur = c.cursor()
    cur.execute(sql, params)
    if fetch:
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        c.close(); return rows
    c.commit(); c.close()

def setup():
    c = conn(); cur = c.cursor()
    try:
        # Criar tabelas principais
        cur.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS horarios (
            id SERIAL PRIMARY KEY, usuario TEXT NOT NULL,
            dia TEXT NOT NULL, inicio TEXT NOT NULL, fim TEXT NOT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS disciplinas (
            id SERIAL PRIMARY KEY, usuario TEXT NOT NULL,
            nome TEXT NOT NULL, prioridade TEXT NOT NULL DEFAULT 'Alta', horas_semana INTEGER NOT NULL)""")

        # Ajustar schema existente de usuarios com colunas extras
        cur.execute("""SELECT column_name, is_nullable
                      FROM information_schema.columns
                      WHERE table_name='usuarios'""")
        cols = {row[0]: row[1] for row in cur.fetchall()}

        if 'usuario' not in cols:
            cur.execute("ALTER TABLE usuarios ADD COLUMN usuario TEXT UNIQUE NOT NULL DEFAULT ''")
        if 'senha' not in cols:
            cur.execute("ALTER TABLE usuarios ADD COLUMN senha TEXT NOT NULL DEFAULT ''")

        # Permitir colunas extras herdadas por compatibilidade
        for extra in cols:
            if extra not in {'id', 'usuario', 'senha'}:
                cur.execute(f"ALTER TABLE usuarios ALTER COLUMN {extra} DROP NOT NULL")

        c.commit()
    except Exception as e:
        st.error(f"Erro ao configurar banco: {e}")
    finally:
        c.close()

setup()

def hash_s(s): return hashlib.sha256(s.encode()).hexdigest()

def cadastrar(nome, u, s):
    try:
        q("INSERT INTO usuarios (nome, usuario, senha) VALUES (%s,%s,%s)", (nome, u, hash_s(s)))
        return True, "Cadastro realizado!"
    except Exception as e:
        if "unique constraint" in str(e).lower():
            return False, "Usuário já existe."
        return False, f"Erro ao cadastrar: {str(e)}"

def logar(u, s):
    try:
        rows = q("SELECT senha FROM usuarios WHERE usuario=%s", (u,), fetch=True)
        if not rows:
            return False
        return rows[0]["senha"] == hash_s(s)
    except Exception as e:
        st.error(f"Erro ao fazer login: {str(e)}")
        return False

if "usuario" not in st.session_state:
    st.session_state.usuario = None

# ── Tela de login ────────────────────────────────────────────────
if not st.session_state.usuario:
    st.markdown("""
    <div style='text-align:center;padding:3rem 0 1.5rem'>
        <h1 style='font-size:2.4rem;color:#6366f1;font-weight:800;margin:0'>📚 Organiza Aí<br>Estudos</h1>
        <p style='color:#6b7280;margin-top:.5rem'>Organize sua rotina de estudos com inteligência</p>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 1.2, 1])[1]
    with col:
        aba = st.radio("", ["🔑 Entrar", "✨ Novo Cadastro"], horizontal=True, label_visibility="collapsed")

        if aba == "🔑 Entrar":
            st.markdown("### Bem-vindo de volta!")
            u = st.text_input("Usuário", placeholder="seu_usuario")
            s = st.text_input("Senha", type="password", placeholder="••••••••")
            if st.button("Entrar →", use_container_width=True, type="primary"):
                if logar(u, s):
                    st.session_state.usuario = u
                    st.switch_page("pages/inicio.py")
                else:
                    st.error("Usuário ou senha incorretos.")
        else:
            st.markdown("### Crie sua conta")
            nome = st.text_input("Nome", placeholder="Seu nome completo")
            u = st.text_input("Usuário", placeholder="Escolha um usuário")
            s = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
            s2 = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")
            if st.button("Criar conta →", use_container_width=True, type="primary"):
                if not nome or not u or not s: st.error("Preencha todos os campos.")
                elif len(s) < 6: st.error("Senha muito curta.")
                elif s != s2: st.error("As senhas não coincidem.")
                else:
                    ok, msg = cadastrar(nome.strip(), u, s)
                    st.success(msg) if ok else st.error(msg)
    st.stop()

# Se chegou aqui logado mas acessou a raiz, redireciona
st.switch_page("pages/inicio.py")
