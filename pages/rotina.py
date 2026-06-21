import streamlit as st
import horarios
from interface import exibir_sidebar

st.set_page_config(page_title="Rotina · Organiza Aí", page_icon="⏰", layout="wide")
usuario = exibir_sidebar()

st.title("⏰ Rotina Semanal")
st.caption("Cadastre seus horários livres para estudo durante a semana.")

with st.expander("➕ Adicionar horário livre", expanded=True):
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1])
    dia = col1.selectbox("Dia da semana", horarios.DIAS_SEMANA)
    inicio = col2.selectbox("Início", horarios.HORAS_DISPONIVEIS, index=6)
    fim = col3.selectbox("Fim", horarios.HORAS_DISPONIVEIS, index=10)

    col4.markdown("<br>", unsafe_allow_html=True)
    if col4.button("Adicionar", type="primary", use_container_width=True):
        if inicio >= fim:
            st.error("O início deve ser antes do fim.")
        else:
            horarios.adicionar_horario(usuario, dia, inicio, fim)
            st.rerun()

st.markdown("### 📅 Seus horários cadastrados")
lista = horarios.obter_horarios(usuario)

if not lista:
    st.info("Nenhum horário cadastrado ainda.")
else:
    for h in lista:
        col1, col2 = st.columns([5, 1])
        col1.write(f"**{h['dia']}** — {h['inicio']} às {h['fim']} ({horarios.duracao_formatada(h['inicio'], h['fim'])})")
        if col2.button("Remover", key=f"r{h['id']}"):
            horarios.excluir_horario(h["id"])
            st.rerun()
