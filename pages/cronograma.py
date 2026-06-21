import streamlit as st
import cronograma
from interface import exibir_sidebar

st.set_page_config(page_title="Cronograma · Organiza Aí", page_icon="🗓️", layout="wide")
usuario = exibir_sidebar()

st.title("🗓️ Cronograma")
st.caption("Seu cronograma de estudos personalizado.")

if st.button("🔄 Gerar / Recalcular cronograma", type="primary"):
    st.session_state.blocos = cronograma.gerar_cronograma(usuario)

blocos = st.session_state.get("blocos", cronograma.gerar_cronograma(usuario))

if not blocos:
    st.warning("Cadastre seus horários em **Rotina** e suas disciplinas em **Disciplinas** primeiro.")
    st.stop()

dia_atual = None
for bloco in blocos:
    if bloco["dia"] != dia_atual:
        st.subheader(bloco["dia"])
        dia_atual = bloco["dia"]
    st.write(f"🕐 {bloco['inicio']} – {bloco['fim']} &nbsp;·&nbsp; **{bloco['disciplina']}**", unsafe_allow_html=True)

st.divider()
st.markdown("### 📊 Resumo por disciplina")
resumo = cronograma.resumo_por_disciplina(blocos)
colunas = st.columns(min(len(resumo), 4))
for i, (nome, minutos) in enumerate(resumo.items()):
    colunas[i % len(colunas)].metric(nome, f"{minutos // 60}h{minutos % 60:02d}min")

st.divider()
pdf_bytes = cronograma.exportar_pdf(usuario, blocos)
st.download_button("📄 Exportar PDF", data=pdf_bytes, file_name="cronograma.pdf", mime="application/pdf")
