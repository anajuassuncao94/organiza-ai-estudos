import streamlit as st
from utils import sidebar, q

st.set_page_config(page_title="Início · Organiza Aí", page_icon="🏠", layout="wide")
usuario = sidebar()

n_h = q("SELECT COUNT(*) as n FROM horarios WHERE usuario=%s", (usuario,), fetch=True)[0]["n"]
n_d = q("SELECT COUNT(*) as n FROM disciplinas WHERE usuario=%s", (usuario,), fetch=True)[0]["n"]

st.title("Início")
st.caption("Pronto para estudar hoje?")

c1, c2, c3 = st.columns(3)
c1.markdown(f"""<div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:14px;
    padding:1.5rem;color:white;text-align:center'>
    <div style='font-size:2.5rem;font-weight:800'>{n_h}</div>
    <div style='opacity:.85;font-size:.9rem'>Blocos de horário</div></div>""", unsafe_allow_html=True)
c2.markdown(f"""<div style='background:linear-gradient(135deg,#10b981,#059669);border-radius:14px;
    padding:1.5rem;color:white;text-align:center'>
    <div style='font-size:2.5rem;font-weight:800'>{n_d}</div>
    <div style='opacity:.85;font-size:.9rem'>Disciplinas cadastradas</div></div>""", unsafe_allow_html=True)
status = "✅ Pronto!" if n_h > 0 and n_d > 0 else "⏳ Configure"
cor = "#f59e0b" if "Configure" in status else "#3b82f6"
c3.markdown(f"""<div style='background:{cor};border-radius:14px;
    padding:1.5rem;color:white;text-align:center'>
    <div style='font-size:1.6rem;font-weight:800'>{status}</div>
    <div style='opacity:.85;font-size:.9rem'>Status do cronograma</div></div>""", unsafe_allow_html=True)

st.markdown("### 🚀 Como começar")
for icon, titulo, desc, done in [
    ("⏰","Rotina","Cadastre seus horários livres de estudo ao longo da semana.", n_h>0),
    ("📖","Disciplinas","Adicione as matérias que você estuda e defina prioridades.", n_d>0),
    ("🗓️","Cronograma","Gere seu cronograma personalizado e exporte em PDF.", n_h>0 and n_d>0),
]:
    cb = "#10b981" if done else "#6366f1"
    tick = "✅" if done else "○"
    st.markdown(f"""<div style='display:flex;align-items:center;gap:1rem;padding:1rem 1.2rem;
        background:white;border-radius:12px;margin-bottom:.6rem;
        border:1px solid #e5e7eb;border-left:4px solid {cb}'>
        <span style='font-size:1.4rem'>{icon}</span>
        <div style='flex:1'><b>{titulo}</b><br>
        <span style='font-size:.85rem;color:#6b7280'>{desc}</span></div>
        <span>{tick}</span></div>""", unsafe_allow_html=True)
