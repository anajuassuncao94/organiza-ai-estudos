import streamlit as st
import disciplinas
from interface import exibir_sidebar

st.set_page_config(page_title="Disciplinas · Organiza Aí", page_icon="📖", layout="wide")
usuario = exibir_sidebar()

st.title("📖 Disciplinas")
st.caption("Gerencie as matérias que você está estudando.")

with st.expander("➕ Adicionar disciplina", expanded=True):
    col1, col2, col3 = st.columns([3, 1.5, 1])
    nome = col1.text_input("Nome da disciplina", placeholder="Ex: Matemática, Português, Física...")
    prioridade = col2.selectbox("Prioridade", ["🔴 Alta", "🟡 Média", "🟢 Baixa"])
    horas = col3.number_input("Horas/semana", min_value=1, max_value=40, value=2)

    if st.button("Adicionar disciplina", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("Digite o nome da disciplina.")
        else:
            disciplinas.adicionar_disciplina(usuario, nome.strip(), prioridade, horas)
            st.rerun()

st.markdown("### 📋 Suas disciplinas")
lista = disciplinas.obter_disciplinas(usuario)

if not lista:
    st.info("Nenhuma disciplina cadastrada ainda.")
else:
    for d in lista:
        col1, col2 = st.columns([5, 1])
        col1.write(f"**{d['nome']}** — {d['prioridade']} · {d['horas_semana']}h/semana")
        if col2.button("Remover", key=f"r{d['id']}"):
            disciplinas.excluir_disciplina(d["id"])
            st.rerun()
