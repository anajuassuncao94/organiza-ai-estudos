"""auth.py - RF01: Realizar login do usuário"""

import hashlib
import streamlit as st
import database


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar_usuario(usuario, senha):
    if database.buscar_usuario(usuario):
        return False, "Usuário já existe."
    database.criar_usuario(usuario, hash_senha(senha))
    return True, "Cadastro realizado com sucesso!"


def realizar_login(usuario, senha):
    dados = database.buscar_usuario(usuario)
    if dados and dados["senha"] == hash_senha(senha):
        st.session_state.usuario = usuario
        return True, "Login realizado com sucesso!"
    return False, "Usuário ou senha incorretos."


def realizar_logout():
    st.session_state.usuario = None


def usuario_autenticado():
    return st.session_state.get("usuario")
