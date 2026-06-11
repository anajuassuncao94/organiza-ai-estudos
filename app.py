import streamlit as st
import psycopg2
import hashlib
from fpdf import FPDF
import io

st.set_page_config(page_title="Organiza Aí Estudos", page_icon="📚", layout="wide")

st.markdown("""
<style>
/* Sidebar */
section[data-testid="stSidebar"] { background: #fff; border-right: 1px solid #e5e7eb; }
section[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; color: #374151; }
/* Botões */
.stButton > button { border-radius: 8px; font-weight: 600; }
/* Geral */
h1 { font-size: 1.8rem !important; color: #111827; }
</style>
""", unsafe_allow_html=True)

# ── Banco ───────────────────────────────────────────────────────
DB_URL = st.secrets["DATABASE_URL"]

def conn():
    return psycopg2.connect(DB_URL)

def q(sql, params=(), fetch=False):
    c = conn(); cur = c.cursor()
    cur.execute(sql, params)
    if fetch:
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        c.close(); return rows
    c.commit(); c.close()
    return cur.rowcount

def setup():
    c = conn(); cur = c.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY, usuario TEXT UNIQUE NOT NULL, senha TEXT NOT NULL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS horarios (
        id SERIAL PRIMARY KEY, usuario TEXT NOT NULL,
        dia TEXT NOT NULL, inicio TEXT NOT NULL, fim TEXT NOT NULL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS disciplinas (
        id SERIAL PRIMARY KEY, usuario TEXT NOT NULL,
        nome TEXT NOT NULL, prioridade TEXT NOT NULL DEFAULT 'Alta', horas_semana INTEGER NOT NULL)""")
    c.commit(); c.close()

setup()

def hash_s(s): return hashlib.sha256(s.encode()).hexdigest()

def cadastrar(u, s):
    try:
        q("INSERT INTO usuarios (usuario, senha) VALUES (%s,%s)", (u, hash_s(s)))
        return True, "Cadastro realizado!"
    except: return False, "Usuário já existe."

def logar(u, s):
    rows = q("SELECT senha FROM usuarios WHERE usuario=%s", (u,), fetch=True)
    return rows and rows[0]["senha"] == hash_s(s)

# ── Session ─────────────────────────────────────────────────────
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# ── Login / Cadastro ────────────────────────────────────────────
if not st.session_state.usuario:
    st.markdown("""
    <div style='text-align:center; padding: 3rem 0 1.5rem'>
        <h1 style='font-size:2.4rem; color:#6366f1; font-weight:800; margin:0'>📚 Organiza Aí<br>Estudos</h1>
        <p style='color:#6b7280; margin-top:0.5rem'>Organize sua rotina de estudos com inteligência</p>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 1.2, 1])[1]
    with col:
        aba = st.radio("", ["🔑 Entrar", "✨ Novo Cadastro"], horizontal=True, label_visibility="collapsed")

        if aba == "🔑 Entrar":
            st.markdown("### Bem-vindo de volta!")
            u = st.text_input("Usuário", placeholder="seu_usuario")
            s = st.text_input("Senha", type="password", placeholder="••••••••")
            if st.button("Entrar →", use_container_width=True, type="primary"):
                if logar(u, s):
                    st.session_state.usuario = u; st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
        else:
            st.markdown("### Crie sua conta")
            u = st.text_input("Usuário", placeholder="Escolha um usuário")
            s = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
            s2 = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")
            if st.button("Criar conta →", use_container_width=True, type="primary"):
                if not u or not s: st.error("Preencha todos os campos.")
                elif len(s) < 6: st.error("Senha muito curta.")
                elif s != s2: st.error("As senhas não coincidem.")
                else:
                    ok, msg = cadastrar(u, s)
                    st.success(msg) if ok else st.error(msg)
    st.stop()

# ── Sidebar ─────────────────────────────────────────────────────
usuario = st.session_state.usuario
with st.sidebar:
    st.image("https://img.icons8.com/color/96/book-stack.png", width=48)
    st.markdown(f"Olá, **{usuario}** 👋")
    st.divider()
    aba = st.radio("", ["Início", "Rotina", "Disciplinas", "Cronograma"], label_visibility="collapsed")
    st.divider()
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.usuario = None; st.rerun()

DIAS = ["Segunda-feira","Terça-feira","Quarta-feira","Quinta-feira","Sexta-feira","Sábado","Domingo"]
HORAS = [f"{h:02d}:{m:02d}" for h in range(5,24) for m in (0,30)]

def dur(ini, fim):
    a = int(ini[:2])*60+int(ini[3:]); b = int(fim[:2])*60+int(fim[3:])
    d = b - a; return f"{d//60}h" if d%60==0 else f"{d//60}h{d%60:02d}min"

def mins(ini, fim):
    return (int(fim[:2])*60+int(fim[3:])) - (int(ini[:2])*60+int(ini[3:]))

# ── Início ───────────────────────────────────────────────────────
if aba == "Início":
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
        cor_borda = "#10b981" if done else "#6366f1"
        tick = "✅" if done else "○"
        st.markdown(f"""<div style='display:flex;align-items:center;gap:1rem;padding:1rem 1.2rem;
            background:white;border-radius:12px;margin-bottom:.6rem;
            border:1px solid #e5e7eb;border-left:4px solid {cor_borda}'>
            <span style='font-size:1.4rem'>{icon}</span>
            <div style='flex:1'><b>{titulo}</b><br>
            <span style='font-size:.85rem;color:#6b7280'>{desc}</span></div>
            <span>{tick}</span></div>""", unsafe_allow_html=True)

# ── Rotina ───────────────────────────────────────────────────────
elif aba == "Rotina":
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
        cols = st.columns(2)
        ci = 0
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
            <b>Total disponível por semana: {total//60}h {total%60:02d}min</b></div>""",
            unsafe_allow_html=True)
    else:
        st.info("Nenhum horário cadastrado.")

# ── Disciplinas ──────────────────────────────────────────────────
elif aba == "Disciplinas":
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

# ── Cronograma ───────────────────────────────────────────────────
elif aba == "Cronograma":
    st.markdown("## 🗓️ Cronograma")
    st.caption("Seu cronograma de estudos personalizado.")

    horarios = q("SELECT dia,inicio,fim FROM horarios WHERE usuario=%s ORDER BY dia,inicio", (usuario,), fetch=True)
    disciplinas = q("SELECT nome,horas_semana FROM disciplinas WHERE usuario=%s ORDER BY prioridade,nome", (usuario,), fetch=True)

    if not horarios:
        st.warning("📖 Você ainda não cadastrou horários. Vá para **Rotina** e adicione seus horários.")
        st.stop()
    if not disciplinas:
        st.warning("📖 Você ainda não cadastrou disciplinas. Vá para **Disciplinas** e adicione suas matérias.")
        st.stop()

    # Distribuir disciplinas nos horários
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
        d = dur(b["ini"],b["fim"])
        st.markdown(f"""<div style='background:#f8fafc;border-left:4px solid #6366f1;
            padding:.6rem 1rem;border-radius:8px;margin-bottom:.4rem;font-size:.95rem'>
            🕐 {b['ini']} – {b['fim']} &nbsp;·&nbsp; <b>{b['disc']}</b>
            <span style='color:#6366f1;float:right'>{d}</span></div>""", unsafe_allow_html=True)

    # Resumo
    resumo = {}
    for b in cronograma: resumo[b["disc"]] = resumo.get(b["disc"],0)+b["min"]
    if resumo:
        st.divider()
        st.markdown("**Resumo por disciplina**")
        cols = st.columns(min(len(resumo),4))
        for i,(nome,m) in enumerate(sorted(resumo.items(), key=lambda x:-x[1])):
            h,mn = m//60, m%60
            cols[i%len(cols)].metric(nome, f"{h}h{mn:02d}min")

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
