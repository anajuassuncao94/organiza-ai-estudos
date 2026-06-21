"""horarios.py - RF03: Cadastrar horários livres"""

import database

DIAS_SEMANA = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
               "Sexta-feira", "Sábado", "Domingo"]

HORAS_DISPONIVEIS = [f"{h:02d}:{m:02d}" for h in range(5, 24) for m in (0, 30)]


def para_minutos(horario):
    h, m = horario.split(":")
    return int(h) * 60 + int(m)


def duracao_formatada(inicio, fim):
    minutos = para_minutos(fim) - para_minutos(inicio)
    return f"{minutos // 60}h{minutos % 60:02d}min" if minutos % 60 else f"{minutos // 60}h"


def adicionar_horario(usuario, dia, inicio, fim):
    database.salvar_horario(usuario, dia, inicio, fim)


def obter_horarios(usuario):
    return database.listar_horarios(usuario)


def excluir_horario(horario_id):
    database.remover_horario(horario_id)
