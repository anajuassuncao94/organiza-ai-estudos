"""disciplinas.py - RF02: Cadastrar disciplinas"""

import database


def adicionar_disciplina(usuario, nome, prioridade, horas_semana):
    database.salvar_disciplina(usuario, nome, prioridade, horas_semana)


def obter_disciplinas(usuario):
    return database.listar_disciplinas(usuario)

def editar_disciplina(disciplina_id, nome, prioridade, horas_semana):
    database.atualizar_disciplina(disciplina_id, nome, prioridade, horas_semana)

def excluir_disciplina(disciplina_id):
    database.remover_disciplina(disciplina_id)
