"""database.py - RF07: Armazenar dados do sistema"""

import psycopg2
import streamlit as st

DB_URL = st.secrets["DATABASE_URL"]


def executar(sql, params=(), fetch=False):
    conexao = psycopg2.connect(DB_URL)
    cursor = conexao.cursor()
    cursor.execute(sql, params)
    if fetch:
        colunas = [c[0] for c in cursor.description]
        resultado = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        conexao.close()
        return resultado
    conexao.commit()
    conexao.close()


def inicializar_banco():
    executar("""CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY, usuario TEXT UNIQUE, senha TEXT)""")
    executar("""CREATE TABLE IF NOT EXISTS horarios (
        id SERIAL PRIMARY KEY, usuario TEXT, dia TEXT, inicio TEXT, fim TEXT)""")
    executar("""CREATE TABLE IF NOT EXISTS disciplinas (
        id SERIAL PRIMARY KEY, usuario TEXT, nome TEXT, prioridade TEXT, horas_semana INTEGER)""")
    executar("""CREATE TABLE IF NOT EXISTS cronogramas (
        id SERIAL PRIMARY KEY, usuario TEXT, dia TEXT, inicio TEXT, fim TEXT, disciplina TEXT)""")


# Usuários
def criar_usuario(usuario, senha_hash):
    executar("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (usuario, senha_hash))


def buscar_usuario(usuario):
    resultado = executar("SELECT usuario, senha FROM usuarios WHERE usuario = %s", (usuario,), fetch=True)
    return resultado[0] if resultado else None


# Disciplinas
def salvar_disciplina(usuario, nome, prioridade, horas_semana):
    executar("INSERT INTO disciplinas (usuario, nome, prioridade, horas_semana) VALUES (%s,%s,%s,%s)",
              (usuario, nome, prioridade, horas_semana))


def listar_disciplinas(usuario):
    return executar("SELECT id, nome, prioridade, horas_semana FROM disciplinas WHERE usuario=%s ORDER BY nome",
                     (usuario,), fetch=True)


def remover_disciplina(disciplina_id):
    executar("DELETE FROM disciplinas WHERE id = %s", (disciplina_id,))


# Horários
def salvar_horario(usuario, dia, inicio, fim):
    executar("INSERT INTO horarios (usuario, dia, inicio, fim) VALUES (%s,%s,%s,%s)",
              (usuario, dia, inicio, fim))


def listar_horarios(usuario):
    return executar("SELECT id, dia, inicio, fim FROM horarios WHERE usuario=%s ORDER BY dia, inicio",
                     (usuario,), fetch=True)


def remover_horario(horario_id):
    executar("DELETE FROM horarios WHERE id = %s", (horario_id,))


# Cronograma
def salvar_cronograma(usuario, blocos):
    executar("DELETE FROM cronogramas WHERE usuario = %s", (usuario,))
    for b in blocos:
        executar("INSERT INTO cronogramas (usuario, dia, inicio, fim, disciplina) VALUES (%s,%s,%s,%s,%s)",
                  (usuario, b["dia"], b["inicio"], b["fim"], b["disciplina"]))
