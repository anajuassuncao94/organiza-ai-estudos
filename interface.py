"""interface.py - sidebar de navegação compartilhada entre as páginas"""

import streamlit as st
import auth


def exibir_sidebar():
    st.markdown("<style>[data-testid='stSidebarNav']{display:none}</style>", unsafe_allow_html=True)

    usuario = auth.usuario_autenticado()
    if not usuario:
        st.switch_page("app.py")

    with st.sidebar:
        st.markdown("### 📚 Organiza Aí Estudos")
        st.write(f"Olá, **{usuario}** 👋")
        st.divider()
        if st.button("🏠 Início", use_container_width=True):
            st.switch_page("pages/inicio.py")
        if st.button("⏰ Rotina", use_container_width=True):
            st.switch_page("pages/rotina.py")
        if st.button("📖 Disciplinas", use_container_width=True):
            st.switch_page("pages/disciplinas.py")
        if st.button("🗓️ Cronograma", use_container_width=True):
            st.switch_page("pages/cronograma.py")
        st.divider()
        if st.button("🚪 Sair", use_container_width=True):
            auth.realizar_logout()
            st.switch_page("app.py")

    return usuario
