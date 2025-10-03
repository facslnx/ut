import streamlit as st
import hashlib
import re
from datetime import datetime, date
import pandas as pd

def setup_page_config():
    """Configuração da página Streamlit"""
    # CSS personalizado para tema escuro
    st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    .stApp {
        background-color: #000000;
    }
    .stSidebar {
        background-color: #1a1a1a;
    }
    .metric-card {
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ff0000;
        margin: 0.5rem 0;
    }
    .primary-button {
        background-color: #ff0000;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
    }
    .card {
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ff0000;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def check_authentication(allow_public=False):
    """Verificar se o usuário está autenticado"""
    if 'user_id' not in st.session_state:
        if allow_public:
            return False  # Permite acesso público
        show_login()
        return False
    return True

def show_login():
    """Mostrar tela de login"""
    # Logo e título centralizados
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="app/static/logo.png" alt="UT-SOCIOS" style="width: 120px; height: 120px; margin-bottom: 15px;">
        <h2 style="color: #ffffff; margin: 10px 0;">UT-SOCIOS</h2>
        <p style="color: #888; margin: 0;">Sistema de Gestão de Sócios</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            
            col_login, col_cadastro = st.columns(2)
            
            with col_login:
                if st.form_submit_button("🔑 Entrar", use_container_width=True):
                    if authenticate_user(email, senha):
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Email ou senha incorretos!")
            
            with col_cadastro:
                if st.form_submit_button("👤 Novo Sócio", use_container_width=True):
                    st.session_state['page'] = 'cadastro_publico'
                    st.rerun()

def authenticate_user(email, senha):
    """Autenticar usuário"""
    from config.database import db
    
    query = "SELECT id, nome, email, senha FROM usuarios WHERE email = %s"
    user = db.execute_query_one(query, (email,))
    
    if user:
        # user é uma tupla: (id, nome, email, senha)
        # Converter para dicionário para facilitar acesso
        user_dict = {
            'id': user[0],
            'nome': user[1], 
            'email': user[2],
            'senha': user[3]
        }
        
        if verify_password(senha, user_dict['senha']):
            st.session_state['user_id'] = user_dict['id']
            st.session_state['username'] = user_dict['nome']
            st.session_state['email'] = user_dict['email']
            return True
    return False

def verify_password(password, hashed_password):
    """Verificar senha hash"""
    try:
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Erro ao verificar senha: {e}")
        return False

def hash_password(password):
    """Hash da senha"""
    try:
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except Exception as e:
        print(f"Erro ao gerar hash da senha: {e}")
        return None

def format_date(date_obj):
    """Formatar data para exibição"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except:
            return date_obj
    if isinstance(date_obj, date):
        return date_obj.strftime('%d/%m/%Y')
    return str(date_obj)

def format_currency(value):
    """Formatar valor monetário"""
    if value is None:
        return "R$ 0,00"
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return f"R$ {value}"

def show_success(message):
    """Mostrar mensagem de sucesso"""
    st.success(message)

def show_error(message):
    """Mostrar mensagem de erro"""
    st.error(message)

def show_warning(message):
    """Mostrar mensagem de aviso"""
    st.warning(message)

def show_info(message):
    """Mostrar mensagem informativa"""
    st.info(message)

def validate_cpf(cpf):
    """Validar CPF"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
    
    # Verificar se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcular primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        return False
    
    # Calcular segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    return int(cpf[10]) == digito2

def format_currency(value):
    """Formatar valor monetário"""
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def format_date(date_obj):
    """Formatar data"""
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
    return date_obj.strftime('%d/%m/%Y')

def show_success(message):
    """Mostrar mensagem de sucesso"""
    st.success(message)

def show_error(message):
    """Mostrar mensagem de erro"""
    st.error(message)

def show_warning(message):
    """Mostrar mensagem de aviso"""
    st.warning(message)

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Criar card de métrica"""
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #ff0000; margin: 0;">{title}</h3>
        <h1 style="color: #ffffff; margin: 0.5rem 0;">{value}</h1>
        {f'<p style="color: #888; margin: 0;">{delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def create_card(title, content):
    """Criar card genérico"""
    st.markdown(f"""
    <div class="card">
        <h3 style="color: #ff0000; margin: 0 0 1rem 0;">{title}</h3>
        <div style="color: #ffffff;">{content}</div>
    </div>
    """, unsafe_allow_html=True)
