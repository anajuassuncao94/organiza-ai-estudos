import streamlit as st
from utils import sidebar, q

st.set_page_config(page_title="Disciplinas · Organiza Aí", page_icon="📖", layout="wide")
usuario = sidebar()

st.markdown("## 📖 Disciplinas")
st.caption("Gerencie as matérias que você está estudando.")

with st.expander("➕ Adicionar disciplina", expanded=True):
    c1,c2,c3 = st.columns([3,1.5,1])
    nome = c1.text_input("Nome da disciplina", placeholder="Ex: Matemática, Português, Física...")
    prio = c2.selectbox("Prioridade", ["🔴 Alta","🟡 Média","🟢 Baixa"])
    horas = c3.number_input("Horas/sem", min_value=1, max_value=40, value=2)
    if st.button("Adicionar disciplina", type="primary", use_container_width=True):
        if not nome.strip(): st.error("Digite o nome.")
        else:
            q("INSERT INTO disciplinas (usuario,nome,prioridade,horas_semana) VALUES (%s,%s,%s,%s)",
              (usuario, nome.strip(), prio, horas))
            st.success("Adicionada!"); st.rerun()

disciplinas = q("SELECT id,nome,prioridade,horas_semana FROM disciplinas WHERE usuario=%s ORDER BY nome",
                (usuario,), fetch=True)

st.markdown("### 📋 Suas disciplinas")
if disciplinas:
    for d in disciplinas:
        c1,c2 = st.columns([6,1])
        c1.markdown(f"**{d['nome']}** — {d['prioridade']} · {d['horas_semana']}h/semana")
        if c2.button("🗑️", key=f"rd{d['id']}"):
            q("DELETE FROM disciplinas WHERE id=%s", (d["id"],)); st.rerun()
else:
    st.info("Nenhuma disciplina cadastrada ainda.")
