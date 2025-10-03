import streamlit as st
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config.database import Database
    from utils.helpers import setup_page_config, check_authentication
    from pages import dashboard, socios, comandos, faturas, usuarios
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.error("Execute: python instalacao.py")
    st.stop()

# Configurar página para não mostrar menu de navegação
st.set_page_config(
    page_title="UT-SOCIOS",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para esconder menu de navegação padrão e sidebar durante login
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Esconder menu de navegação padrão */
.stApp > div:first-child > div:first-child > div:first-child {
    display: none;
}

/* Esconder menu de navegação lateral padrão */
.stApp > div:first-child > div:first-child > div:first-child > div:first-child {
    display: none;
}

/* Esconder sidebar durante login */
.stApp > div:first-child > div:first-child > div:last-child {
    display: none;
}

/* Centralizar conteúdo durante login */
.stApp > div:first-child > div:first-child > div:first-child {
    width: 100% !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Configuração da página
    setup_page_config()
    
    # Verificar autenticação
    if not check_authentication():
        return
    
    # Sidebar de navegação
    with st.sidebar:
        # Logo usando logo.png
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="assets/logo.png" alt="UT-SOCIOS" style="width: 80px; height: 80px; margin-bottom: 10px;">
            <h2 style="color: #ffffff; margin: 5px 0;">UT-SOCIOS</h2>
            <p style="color: #888; margin: 0;">Sistema de Gestão</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # Menu de navegação
        page = st.selectbox(
            "Navegação",
            ["🏠 Dashboard", "👥 Sócios", "🏛️ Comandos", "💰 Faturas", "👤 Usuários"],
            index=0
        )
        
        st.markdown("---")
        st.markdown(f"**Usuário:** {st.session_state.get('username', 'N/A')}")
        
        if st.button("🚪 Sair"):
            st.session_state.clear()
            st.rerun()
    
    # Roteamento de páginas
    if page == "🏠 Dashboard":
        dashboard.show()
    elif page == "👥 Sócios":
        socios.show()
    elif page == "🏛️ Comandos":
        comandos.show()
    elif page == "💰 Faturas":
        faturas.show()
    elif page == "👤 Usuários":
        usuarios.show()

if __name__ == "__main__":
    main()
