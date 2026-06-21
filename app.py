"""app.py - tela de login e cadastro (RF01)"""

import streamlit as st
import database
import auth

st.set_page_config(page_title="Organiza Aí Estudos", page_icon="📚", layout="wide")
st.markdown("<style>[data-testid='stSidebarNav']{display:none}</style>", unsafe_allow_html=True)

database.inicializar_banco()

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario:
    st.switch_page("pages/inicio.py")

st.markdown("""
<div style='text-align:center; padding:3rem 0 1.5rem'>
    <h1 style='font-size:2.4rem; color:#6366f1; font-weight:800; margin:0'>📚 Organiza Aí<br>Estudos</h1>
    <p style='color:#6b7280; margin-top:.5rem'>Organize sua rotina de estudos com inteligência</p>
</div>
""", unsafe_allow_html=True)

col = st.columns([1, 1.2, 1])[1]
with col:
    aba = st.radio("", ["🔑 Entrar", "✨ Novo Cadastro"], horizontal=True, label_visibility="collapsed")

    if aba == "🔑 Entrar":
        st.markdown("### Bem-vindo de volta!")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar →", type="primary", use_container_width=True):
            ok, msg = auth.realizar_login(usuario, senha)
            st.switch_page("pages/inicio.py") if ok else st.error(msg)

    else:
        st.markdown("### Crie sua conta")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        confirmar = st.text_input("Confirmar senha", type="password")
        if st.button("Criar conta →", type="primary", use_container_width=True):
            if senha != confirmar:
                st.error("As senhas não coincidem.")
            else:
                ok, msg = auth.cadastrar_usuario(usuario, senha)
                st.success(msg) if ok else st.error(msg)
