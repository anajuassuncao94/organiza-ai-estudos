import streamlit as st
from utils import sidebar, q, dur, mins, DIAS, HORAS

st.set_page_config(page_title="Rotina · Organiza Aí", page_icon="⏰", layout="wide")
usuario = sidebar()

st.markdown("## ⏰ Rotina Semanal")
st.caption("Cadastre seus horários livres para estudo durante a semana.")

with st.expander("➕ Adicionar horário livre", expanded=True):
    c1,c2,c3,c4 = st.columns([3,1.5,1.5,1])
    dia = c1.selectbox("Dia da semana", DIAS)
    ini = c2.selectbox("Início", HORAS, index=HORAS.index("08:00"))
    fim = c3.selectbox("Fim", HORAS, index=HORAS.index("10:00"))
    c4.markdown("<br>", unsafe_allow_html=True)
    if c4.button("Adicionar", type="primary", use_container_width=True):
        if ini >= fim: st.error("Início deve ser antes do fim.")
        else:
            q("INSERT INTO horarios (usuario,dia,inicio,fim) VALUES (%s,%s,%s,%s)", (usuario,dia,ini,fim))
            st.success("Adicionado!"); st.rerun()

horarios = q("SELECT id,dia,inicio,fim FROM horarios WHERE usuario=%s ORDER BY dia,inicio", (usuario,), fetch=True)

if horarios:
    st.markdown("### 📅 Seus horários cadastrados")
    por_dia = {d:[] for d in DIAS}
    for h in horarios: por_dia[h["dia"]].append(h)
    cols = st.columns(2); ci = 0
    for dia in DIAS:
        if not por_dia[dia]: continue
        with cols[ci%2]:
            st.markdown(f"**{dia}**")
            for h in por_dia[dia]:
                a,b = st.columns([5,1])
                a.markdown(f"""<div style='background:#f0f4ff;border-left:3px solid #6366f1;
                    padding:.5rem .8rem;border-radius:6px;margin-bottom:.3rem;font-size:.9rem'>
                    🕐 {h['inicio']} – {h['fim']}
                    <span style='color:#6366f1'> ({dur(h['inicio'],h['fim'])})</span></div>""",
                    unsafe_allow_html=True)
                if b.button("🗑️", key=f"rh{h['id']}"):
                    q("DELETE FROM horarios WHERE id=%s", (h["id"],)); st.rerun()
        ci += 1
    total = sum(mins(h["inicio"],h["fim"]) for h in horarios)
    st.markdown(f"""<div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;
        border-radius:12px;padding:1rem;text-align:center;margin-top:1rem'>
        <b>Total disponível por semana: {total//60}h {total%60:02d}min</b></div>""", unsafe_allow_html=True)
else:
    st.info("Nenhum horário cadastrado.")
