import streamlit as st
import database
from interface import exibir_sidebar

st.set_page_config(page_title="Início · Organiza Aí", page_icon="🏠", layout="wide")
usuario = exibir_sidebar()

st.title("Início")
st.caption("Pronto para estudar hoje?")

total_horarios = len(database.listar_horarios(usuario))
total_disciplinas = len(database.listar_disciplinas(usuario))

col1, col2, col3 = st.columns(3)
col1.metric("Blocos de horário", total_horarios)
col2.metric("Disciplinas cadastradas", total_disciplinas)
col3.metric("Status", "✅ Pronto" if total_horarios and total_disciplinas else "⏳ Configure")

st.markdown("### 🚀 Como começar")
st.write("1. Vá em **Rotina** e cadastre seus horários livres.")
st.write("2. Vá em **Disciplinas** e cadastre as matérias que você estuda.")
st.write("3. Vá em **Cronograma** para gerar seu plano de estudos e exportar em PDF.")
