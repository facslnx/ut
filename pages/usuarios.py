import streamlit as st
import pandas as pd
from config.database import db
from utils.helpers import show_success, show_error
from utils.validators import validate_email
from utils.helpers import hash_password

def show():
    st.title("👤 Gestão de Usuários")
    st.markdown("---")
    
    # Inicializar session_state se não existir
    if 'usuario_action' not in st.session_state:
        st.session_state['usuario_action'] = 'list'
    
    # Botões de ação
    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.button("➕ Novo Usuário", use_container_width=True, key="btn_novo_usuario"):
            st.session_state['usuario_action'] = 'create'
    
    # Verificar ação e renderizar conteúdo
    action = st.session_state.get('usuario_action', 'list')
    
    if action == 'create':
        show_create_form()
    elif action == 'edit':
        show_edit_form(st.session_state.get('usuario_id'))
    else:
        show_usuarios_list()

def show_usuarios_list():
    """Mostrar lista de usuários"""
    
    # Buscar usuários
    usuarios_query = "SELECT * FROM usuarios ORDER BY nome"
    usuarios = db.execute_query(usuarios_query, fetch=True)
    
    if usuarios:
        st.subheader("📋 Lista de Usuários")
        
        # Mostrar cada usuário em um card
        for usuario in usuarios:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{usuario['nome']}**")
                    st.write(f"📧 {usuario['email']}")
                
                with col2:
                    st.write(f"🆔 ID: {usuario['id']}")
                    st.write(f"📅 Criado: {usuario['created_at'].strftime('%d/%m/%Y')}")
                
                with col3:
                    if usuario['id'] == st.session_state.get('user_id'):
                        st.success("👤 Usuário Atual")
                    else:
                        st.info("👥 Outro Usuário")
                
                with col4:
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️", key=f"edit_{usuario['id']}"):
                            st.session_state['usuario_action'] = 'edit'
                            st.session_state['usuario_id'] = usuario['id']
                            st.rerun()
                    with col_del:
                        if usuario['id'] != st.session_state.get('user_id'):
                            if st.button("🗑️", key=f"del_{usuario['id']}"):
                                if delete_usuario(usuario['id']):
                                    show_success("Usuário excluído com sucesso!")
                                    st.rerun()
                                else:
                                    show_error("Erro ao excluir usuário!")
                        else:
                            st.button("🔒", key=f"locked_{usuario['id']}", disabled=True, help="Não pode excluir seu próprio usuário")
                
                st.markdown("---")
    else:
        st.info("Nenhum usuário encontrado.")

def show_create_form():
    """Mostrar formulário de criação"""
    st.subheader("➕ Novo Usuário")
    
    with st.form("create_usuario_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *")
            email = st.text_input("Email *")
        
        with col2:
            senha = st.text_input("Senha *", type="password")
            confirmar_senha = st.text_input("Confirmar Senha *", type="password")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.form_submit_button("💾 Salvar", use_container_width=True):
                if validate_usuario_form(nome, email, senha, confirmar_senha):
                    if create_usuario(nome, email, senha):
                        show_success("Usuário criado com sucesso!")
                        st.session_state['usuario_action'] = 'list'
                        st.rerun()
                    else:
                        show_error("Erro ao criar usuário!")
                else:
                    show_error("Por favor, preencha todos os campos corretamente!")
        
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state['usuario_action'] = 'list'
                st.rerun()

def show_edit_form(usuario_id):
    """Mostrar formulário de edição"""
    st.subheader("✏️ Editar Usuário")
    
    # Buscar dados do usuário
    usuario_query = "SELECT * FROM usuarios WHERE id = %s"
    usuario = db.execute_query_one(usuario_query, (usuario_id,))
    
    if not usuario:
        show_error("Usuário não encontrado!")
        st.session_state['usuario_action'] = 'list'
        st.rerun()
        return
    
    with st.form("edit_usuario_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *", value=usuario['nome'])
            email = st.text_input("Email *", value=usuario['email'])
        
        with col2:
            senha = st.text_input("Nova Senha (deixe em branco para manter atual)", type="password")
            confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.form_submit_button("💾 Salvar", use_container_width=True):
                if validate_usuario_form(nome, email, senha, confirmar_senha, is_edit=True):
                    if update_usuario(usuario_id, nome, email, senha):
                        show_success("Usuário atualizado com sucesso!")
                        st.session_state['usuario_action'] = 'list'
                        st.rerun()
                    else:
                        show_error("Erro ao atualizar usuário!")
                else:
                    show_error("Por favor, preencha todos os campos corretamente!")
        
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state['usuario_action'] = 'list'
                st.rerun()

def validate_usuario_form(nome, email, senha, confirmar_senha, is_edit=False):
    """Validar formulário de usuário"""
    if not nome or not email:
        return False
    
    if not validate_email(email):
        show_error("Email inválido!")
        return False
    
    if not is_edit and (not senha or not confirmar_senha):
        show_error("Senha é obrigatória para novos usuários!")
        return False
    
    if senha and senha != confirmar_senha:
        show_error("Senhas não coincidem!")
        return False
    
    return True

def create_usuario(nome, email, senha):
    """Criar novo usuário"""
    try:
        # Verificar se email já existe
        email_check_query = "SELECT id FROM usuarios WHERE email = %s"
        existing = db.execute_query_one(email_check_query, (email,))
        
        if existing:
            show_error("Email já cadastrado!")
            return False
        
        # Hash da senha
        senha_hash = hash_password(senha)
        
        # Inserir usuário
        insert_query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        params = (nome, email, senha_hash)
        
        return db.execute_query(insert_query, params)
        
    except Exception as e:
        show_error(f"Erro ao criar usuário: {e}")
        return False

def update_usuario(usuario_id, nome, email, senha):
    """Atualizar usuário"""
    try:
        # Verificar se email já existe em outro usuário
        email_check_query = "SELECT id FROM usuarios WHERE email = %s AND id != %s"
        existing = db.execute_query_one(email_check_query, (email, usuario_id))
        
        if existing:
            show_error("Email já cadastrado em outro usuário!")
            return False
        
        # Preparar query de atualização
        if senha:
            # Atualizar com nova senha
            senha_hash = hash_password(senha)
            update_query = "UPDATE usuarios SET nome = %s, email = %s, senha = %s WHERE id = %s"
            params = (nome, email, senha_hash, usuario_id)
        else:
            # Manter senha atual
            update_query = "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s"
            params = (nome, email, usuario_id)
        
        return db.execute_query(update_query, params)
        
    except Exception as e:
        show_error(f"Erro ao atualizar usuário: {e}")
        return False

def delete_usuario(usuario_id):
    """Excluir usuário"""
    try:
        # Verificar se não é o próprio usuário
        if usuario_id == st.session_state.get('user_id'):
            show_error("Você não pode excluir seu próprio usuário!")
            return False
        
        delete_query = "DELETE FROM usuarios WHERE id = %s"
        return db.execute_query(delete_query, (usuario_id,))
    except Exception as e:
        show_error(f"Erro ao excluir usuário: {e}")
        return False
