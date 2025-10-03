import streamlit as st
import pandas as pd
from config.database import db
from utils.helpers import show_success, show_error

def show():
    st.title("🏛️ Gestão de Comandos")
    st.markdown("---")
    
    # Inicializar session_state se não existir
    if 'comando_action' not in st.session_state:
        st.session_state['comando_action'] = 'list'
    
    # Botões de ação
    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.button("➕ Novo Comando", use_container_width=True, key="btn_novo_comando"):
            st.session_state['comando_action'] = 'create'
    
    # Verificar ação e renderizar conteúdo
    action = st.session_state.get('comando_action', 'list')
    
    if action == 'create':
        show_create_form()
    elif action == 'edit':
        show_edit_form(st.session_state.get('comando_id'))
    else:
        show_comandos_list()

def show_comandos_list():
    """Mostrar lista de comandos"""
    
    # Buscar comandos com contagem de sócios
    comandos_query = """
    SELECT c.*, COUNT(s.id) as total_socios 
    FROM comandos c 
    LEFT JOIN socios s ON c.id = s.comando_id 
    GROUP BY c.id 
    ORDER BY c.nome
    """
    
    comandos = db.execute_query(comandos_query, fetch=True)
    
    if comandos:
        st.subheader("📋 Lista de Comandos")
        
        # Mostrar em cards
        cols = st.columns(3)
        
        for idx, comando in enumerate(comandos):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background-color: #1a1a1a; 
                        padding: 1rem; 
                        border-radius: 0.5rem; 
                        border: 1px solid #ff0000;
                        margin-bottom: 1rem;
                    ">
                        <h3 style="color: #ff0000; margin: 0;">{comando['nome']}</h3>
                        <p style="color: #ffffff; margin: 0.5rem 0;">
                            {comando['total_socios']} sócio{'s' if comando['total_socios'] != 1 else ''}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️", key=f"edit_{comando['id']}"):
                            st.session_state['comando_action'] = 'edit'
                            st.session_state['comando_id'] = comando['id']
                            st.rerun()
                    with col2:
                        if comando['total_socios'] == 0:
                            if st.button("🗑️", key=f"del_{comando['id']}"):
                                if delete_comando(comando['id']):
                                    show_success("Comando excluído com sucesso!")
                                    st.rerun()
                                else:
                                    show_error("Erro ao excluir comando!")
                        else:
                            st.button("🔒", key=f"locked_{comando['id']}", disabled=True, help="Não pode excluir comando com sócios")
    else:
        st.info("Nenhum comando cadastrado ainda.")

def show_create_form():
    """Mostrar formulário de criação"""
    st.subheader("➕ Novo Comando")
    
    with st.form("create_comando_form"):
        nome = st.text_input("Nome do Comando *")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.form_submit_button("💾 Salvar", use_container_width=True):
                if nome and nome.strip():
                    if create_comando(nome):
                        show_success("Comando criado com sucesso!")
                        st.session_state['comando_action'] = 'list'
                        st.rerun()
                    else:
                        show_error("Erro ao criar comando!")
                else:
                    show_error("Nome do comando é obrigatório!")
        
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state['comando_action'] = 'list'
                st.rerun()

def show_edit_form(comando_id):
    """Mostrar formulário de edição"""
    st.subheader("✏️ Editar Comando")
    
    # Buscar dados do comando
    comando_query = "SELECT * FROM comandos WHERE id = %s"
    comando = db.execute_query_one(comando_query, (comando_id,))
    
    if not comando:
        show_error("Comando não encontrado!")
        st.session_state['comando_action'] = 'list'
        st.rerun()
        return
    
    with st.form("edit_comando_form"):
        nome = st.text_input("Nome do Comando *", value=comando['nome'])
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.form_submit_button("💾 Salvar", use_container_width=True):
                if nome and nome.strip():
                    if update_comando(comando_id, nome):
                        show_success("Comando atualizado com sucesso!")
                        st.session_state['comando_action'] = 'list'
                        st.rerun()
                    else:
                        show_error("Erro ao atualizar comando!")
                else:
                    show_error("Nome do comando é obrigatório!")
        
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state['comando_action'] = 'list'
                st.rerun()

def create_comando(nome):
    """Criar novo comando"""
    try:
        insert_query = "INSERT INTO comandos (nome) VALUES (%s)"
        return db.execute_query(insert_query, (nome,))
    except Exception as e:
        show_error(f"Erro ao criar comando: {e}")
        return False

def update_comando(comando_id, nome):
    """Atualizar comando"""
    try:
        update_query = "UPDATE comandos SET nome = %s WHERE id = %s"
        return db.execute_query(update_query, (nome, comando_id))
    except Exception as e:
        show_error(f"Erro ao atualizar comando: {e}")
        return False

def delete_comando(comando_id):
    """Excluir comando"""
    try:
        delete_query = "DELETE FROM comandos WHERE id = %s"
        return db.execute_query(delete_query, (comando_id,))
    except Exception as e:
        show_error(f"Erro ao excluir comando: {e}")
        return False
