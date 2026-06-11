import streamlit as st
import psycopg2
import hashlib

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

def dur(ini, fim):
    a = int(ini[:2])*60+int(ini[3:]); b = int(fim[:2])*60+int(fim[3:])
    d = b-a; return f"{d//60}h" if d%60==0 else f"{d//60}h{d%60:02d}min"

def mins(ini, fim):
    return (int(fim[:2])*60+int(fim[3:])) - (int(ini[:2])*60+int(ini[3:]))

DIAS = ["Segunda-feira","Terça-feira","Quarta-feira","Quinta-feira","Sexta-feira","Sábado","Domingo"]
HORAS = [f"{h:02d}:{m:02d}" for h in range(5,24) for m in (0,30)]

def sidebar():
    """Renderiza sidebar e retorna usuario. Redireciona se não logado."""
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    if not st.session_state.get("usuario"):
        st.switch_page("app.py")

    usuario = st.session_state.usuario
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/book-stack.png", width=48)
        st.markdown(f"Olá, **{usuario}** 👋")
        st.divider()
        if st.button("🏠 Início",      use_container_width=True): st.switch_page("pages/inicio.py")
        if st.button("⏰ Rotina",      use_container_width=True): st.switch_page("pages/rotina.py")
        if st.button("📖 Disciplinas", use_container_width=True): st.switch_page("pages/disciplinas.py")
        if st.button("🗓️ Cronograma", use_container_width=True): st.switch_page("pages/cronograma.py")
        st.divider()
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.usuario = None
            st.switch_page("app.py")
    return usuario
