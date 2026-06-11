import json
import os
from contextlib import contextmanager
from datetime import date
from typing import Any, Iterable

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st


DIAS_SEMANA = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]


def get_database_url() -> str:
    try:
        url = st.secrets.get("DATABASE_URL")
        if url:
            return str(url)
    except Exception:
        pass

    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL não configurada. Configure em .streamlit/secrets.toml ou variável de ambiente."
        )
    return url


@contextmanager
def get_connection():
    url = get_database_url()
    kwargs: dict[str, Any] = {}
    if "render.com" in url and "sslmode=" not in url:
        kwargs["sslmode"] = "require"

    conn = psycopg2.connect(url, **kwargs)
    try:
        yield conn
    finally:
        conn.close()


def execute(sql: str, params: Iterable[Any] | None = None, fetchone: bool = False, fetchall: bool = False):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            result = None
            if fetchone:
                result = cur.fetchone()
            elif fetchall:
                result = cur.fetchall()
            conn.commit()
            return result


def init_db() -> None:
    execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(80) UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS disciplinas (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            nome VARCHAR(160) NOT NULL,
            cor VARCHAR(40) NOT NULL DEFAULT 'Azul',
            criada_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS horarios_livres (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            dia_semana VARCHAR(30) NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME NOT NULL,
            criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS cronogramas (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            itens JSONB NOT NULL DEFAULT '[]'::jsonb
        );
        """
    )


def create_user(usuario: str, senha_hash: str):
    return execute(
        """
        INSERT INTO usuarios (usuario, senha_hash)
        VALUES (%s, %s)
        RETURNING id, usuario;
        """,
        (usuario, senha_hash),
        fetchone=True,
    )


def get_user_by_username(usuario: str):
    return execute(
        """
        SELECT id, usuario, senha_hash
        FROM usuarios
        WHERE LOWER(usuario) = LOWER(%s);
        """,
        (usuario,),
        fetchone=True,
    )


def add_disciplina(usuario_id: int, nome: str, cor: str):
    return execute(
        """
        INSERT INTO disciplinas (user_id, nome, cor)
        VALUES (%s, %s, %s)
        RETURNING *;
        """,
        (usuario_id, nome, cor),
        fetchone=True,
    )


def list_disciplinas(usuario_id: int):
    return execute(
        """
        SELECT id, nome, cor, criada_em
        FROM disciplinas
        WHERE user_id = %s
        ORDER BY nome ASC;
        """,
        (usuario_id,),
        fetchall=True,
    )


def update_disciplina(disciplina_id: int, usuario_id: int, nome: str, cor: str):
    return execute(
        """
        UPDATE disciplinas
        SET nome = %s, cor = %s
        WHERE id = %s AND user_id = %s
        RETURNING *;
        """,
        (nome, cor, disciplina_id, usuario_id),
        fetchone=True,
    )


def delete_disciplina(disciplina_id: int, usuario_id: int):
    return execute(
        """
        DELETE FROM disciplinas
        WHERE id = %s AND user_id = %s
        RETURNING id;
        """,
        (disciplina_id, usuario_id),
        fetchone=True,
    )


def add_horario(usuario_id: int, dia_semana: str, hora_inicio: str, hora_fim: str):
    return execute(
        """
        INSERT INTO horarios_livres (usuario_id, dia_semana, hora_inicio, hora_fim)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """,
        (usuario_id, dia_semana, hora_inicio, hora_fim),
        fetchone=True,
    )


def list_horarios(usuario_id: int):
    rows = execute(
        """
        SELECT id, dia_semana, hora_inicio, hora_fim, criado_em
        FROM horarios_livres
        WHERE usuario_id = %s
        ORDER BY
            CASE dia_semana
                WHEN 'Segunda-feira' THEN 1
                WHEN 'Terça-feira' THEN 2
                WHEN 'Quarta-feira' THEN 3
                WHEN 'Quinta-feira' THEN 4
                WHEN 'Sexta-feira' THEN 5
                WHEN 'Sábado' THEN 6
                WHEN 'Domingo' THEN 7
                ELSE 8
            END,
            hora_inicio ASC;
        """,
        (usuario_id,),
        fetchall=True,
    )
    return rows or []


def update_horario(horario_id: int, usuario_id: int, dia_semana: str, hora_inicio: str, hora_fim: str):
    return execute(
        """
        UPDATE horarios_livres
        SET dia_semana = %s, hora_inicio = %s, hora_fim = %s
        WHERE id = %s AND usuario_id = %s
        RETURNING *;
        """,
        (dia_semana, hora_inicio, hora_fim, horario_id, usuario_id),
        fetchone=True,
    )


def delete_horario(horario_id: int, usuario_id: int):
    return execute(
        """
        DELETE FROM horarios_livres
        WHERE id = %s AND usuario_id = %s
        RETURNING id;
        """,
        (horario_id, usuario_id),
        fetchone=True,
    )


def save_cronograma(usuario_id: int, itens: list[dict[str, Any]]):
    return execute(
        """
        INSERT INTO cronogramas (usuario_id, itens)
        VALUES (%s, %s::jsonb)
        RETURNING *;
        """,
        (usuario_id, json.dumps(itens, ensure_ascii=False)),
        fetchone=True,
    )


def get_latest_cronograma(usuario_id: int):
    row = execute(
        """
        SELECT id, usuario_id, data_criacao, itens
        FROM cronogramas
        WHERE usuario_id = %s
        ORDER BY data_criacao DESC
        LIMIT 1;
        """,
        (usuario_id,),
        fetchone=True,
    )
    if row and isinstance(row.get("itens"), str):
        row["itens"] = json.loads(row["itens"])
    return row


def count_blocos_horario(usuario_id: int) -> int:
    horarios = list_horarios(usuario_id)
    return len(horarios)


def count_disciplinas(usuario_id: int) -> int:
    row = execute(
        "SELECT COUNT(*) AS total FROM disciplinas WHERE user_id = %s;",
        (usuario_id,),
        fetchone=True,
    )
    return int(row["total"]) if row else 0
