"""cronograma.py - RF04/RF05: Gerar cronograma | RF06: Exportar em PDF"""

from fpdf import FPDF
import database
from horarios import DIAS_SEMANA, para_minutos


def gerar_cronograma(usuario):
    horarios = database.listar_horarios(usuario)
    disciplinas = database.listar_disciplinas(usuario)
    if not horarios or not disciplinas:
        return []

    restante = [d["horas_semana"] * 60 for d in disciplinas]
    i = 0
    blocos = []

    for h in sorted(horarios, key=lambda x: (DIAS_SEMANA.index(x["dia"]), x["inicio"])):
        atual = para_minutos(h["inicio"])
        fim = para_minutos(h["fim"])

        while atual < fim and i < len(disciplinas):
            usar = min(restante[i], fim - atual, 120)
            if usar <= 0:
                i += 1
                continue
            blocos.append({
                "dia": h["dia"],
                "inicio": f"{atual//60:02d}:{atual%60:02d}",
                "fim": f"{(atual+usar)//60:02d}:{(atual+usar)%60:02d}",
                "disciplina": disciplinas[i]["nome"],
            })
            restante[i] -= usar
            if restante[i] <= 0:
                i += 1
            atual += usar

    database.salvar_cronograma(usuario, blocos)
    return blocos


def resumo_por_disciplina(blocos):
    resumo = {}
    for b in blocos:
        minutos = para_minutos(b["fim"]) - para_minutos(b["inicio"])
        resumo[b["disciplina"]] = resumo.get(b["disciplina"], 0) + minutos
    return resumo


def exportar_pdf(usuario, blocos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Cronograma de Estudos", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Usuário: {usuario}", ln=True)
    pdf.ln(4)

    dia_atual = None
    for b in blocos:
        if b["dia"] != dia_atual:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, b["dia"], ln=True)
            pdf.set_font("Helvetica", "", 11)
            dia_atual = b["dia"]
        pdf.cell(0, 7, f"  {b['inicio']} - {b['fim']}   {b['disciplina']}", ln=True)

    return bytes(pdf.output())
