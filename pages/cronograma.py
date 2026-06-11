import streamlit as st
import io
from fpdf import FPDF
from utils import sidebar, q, dur, DIAS

st.set_page_config(page_title="Cronograma · Organiza Aí", page_icon="🗓️", layout="wide")
usuario = sidebar()

st.markdown("## 🗓️ Cronograma")
st.caption("Seu cronograma de estudos personalizado.")

horarios = q("SELECT dia,inicio,fim FROM horarios WHERE usuario=%s ORDER BY dia,inicio", (usuario,), fetch=True)
disciplinas = q("SELECT nome,horas_semana FROM disciplinas WHERE usuario=%s ORDER BY prioridade,nome", (usuario,), fetch=True)

if not horarios:
    st.warning("Cadastre seus horários em **Rotina** primeiro."); st.stop()
if not disciplinas:
    st.warning("Cadastre suas disciplinas em **Disciplinas** primeiro."); st.stop()

# Gerar cronograma
cronograma = []
disc_idx = 0
restante = [d["horas_semana"]*60 for d in disciplinas]

for h in sorted(horarios, key=lambda x: (DIAS.index(x["dia"]) if x["dia"] in DIAS else 99, x["inicio"])):
    cur = int(h["inicio"][:2])*60+int(h["inicio"][3:])
    fim_m = int(h["fim"][:2])*60+int(h["fim"][3:])
    while cur < fim_m and disc_idx < len(disciplinas):
        usar = min(restante[disc_idx], fim_m-cur, 120)
        if usar <= 0: disc_idx += 1; continue
        ini_s = f"{cur//60:02d}:{cur%60:02d}"
        fim_s = f"{(cur+usar)//60:02d}:{(cur+usar)%60:02d}"
        cronograma.append({"dia":h["dia"],"ini":ini_s,"fim":fim_s,
                           "disc":disciplinas[disc_idx]["nome"],"min":usar})
        restante[disc_idx] -= usar
        if restante[disc_idx] <= 0: disc_idx += 1
        cur += usar

# Exibir
dia_atual = None
for b in cronograma:
    if b["dia"] != dia_atual:
        st.subheader(b["dia"]); dia_atual = b["dia"]
    st.markdown(f"""<div style='background:#f8fafc;border-left:4px solid #6366f1;
        padding:.6rem 1rem;border-radius:8px;margin-bottom:.4rem;font-size:.95rem'>
        🕐 {b['ini']} – {b['fim']} &nbsp;·&nbsp; <b>{b['disc']}</b>
        <span style='color:#6366f1;float:right'>{dur(b['ini'],b['fim'])}</span></div>""",
        unsafe_allow_html=True)

# Resumo
resumo = {}
for b in cronograma: resumo[b["disc"]] = resumo.get(b["disc"],0)+b["min"]
if resumo:
    st.divider()
    st.markdown("**Resumo por disciplina**")
    cols = st.columns(min(len(resumo),4))
    for i,(nome,m) in enumerate(sorted(resumo.items(), key=lambda x:-x[1])):
        cols[i%len(cols)].metric(nome, f"{m//60}h{m%60:02d}min")

# PDF
st.divider()
if st.button("📄 Exportar PDF", type="primary"):
    pdf = FPDF(); pdf.add_page()
    pdf.set_font("Helvetica","B",16)
    pdf.cell(0,10,"Cronograma de Estudos",ln=True)
    pdf.set_font("Helvetica","",11); pdf.ln(3)
    dia_atual = None
    for b in cronograma:
        if b["dia"] != dia_atual:
            pdf.set_font("Helvetica","B",12); pdf.ln(4)
            pdf.cell(0,8,b["dia"],ln=True)
            pdf.set_font("Helvetica","",11); dia_atual = b["dia"]
        pdf.cell(0,7,f"  {b['ini']} - {b['fim']}   {b['disc']}",ln=True)
    buf = io.BytesIO(pdf.output())
    st.download_button("⬇️ Baixar PDF", data=buf, file_name="cronograma.pdf", mime="application/pdf")
