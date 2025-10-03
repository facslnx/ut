#!/usr/bin/env python3
"""
Script para Corrigir Erros Comuns - UT-SOCIOS
Resolve problemas de execução automaticamente
"""

import os
import sys
import subprocess

def create_missing_directories():
    """Criar diretórios ausentes"""
    print("📁 Criando diretórios ausentes...")
    
    directories = [
        "assets",
        "uploads",
        "uploads/comprovantes",
        ".streamlit"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Pasta {directory} criada")
        else:
            print(f"✅ Pasta {directory} já existe")

def create_env_file():
    """Criar arquivo .env se não existir"""
    print("\n📝 Configurando arquivo .env...")
    
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            try:
                with open("env.example", "r", encoding="utf-8") as src:
                    content = src.read()
                with open(".env", "w", encoding="utf-8") as dst:
                    dst.write(content)
                print("✅ Arquivo .env criado a partir do env.example")
            except Exception as e:
                print(f"❌ Erro ao criar .env: {e}")
        else:
            # Criar .env básico
            env_content = """# Configurações do Banco de Dados
DB_HOST=localhost
DB_NAME=ut_socios
DB_USER=root
DB_PASSWORD=

# Configurações da Aplicação
APP_TITLE=UT-SOCIOS
APP_ICON=⚽
"""
            try:
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(env_content)
                print("✅ Arquivo .env criado com configurações padrão")
            except Exception as e:
                print(f"❌ Erro ao criar .env: {e}")
    else:
        print("✅ Arquivo .env já existe")

def create_streamlit_config():
    """Criar configuração do Streamlit"""
    print("\n⚙️ Configurando Streamlit...")
    
    config_dir = ".streamlit"
    config_file = os.path.join(config_dir, "config.toml")
    
    if not os.path.exists(config_file):
        config_content = """[theme]
primaryColor = "#ff0000"
backgroundColor = "#000000"
secondaryBackgroundColor = "#1a1a1a"
textColor = "#ffffff"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
"""
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                f.write(config_content)
            print("✅ Configuração do Streamlit criada")
        except Exception as e:
            print(f"❌ Erro ao criar config.toml: {e}")
    else:
        print("✅ Configuração do Streamlit já existe")

def fix_import_errors():
    """Corrigir erros de importação"""
    print("\n🔧 Corrigindo erros de importação...")
    
    # Verificar se os módulos podem ser importados
    try:
        import streamlit
        print("✅ Streamlit - OK")
    except ImportError:
        print("❌ Streamlit não encontrado - Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit==1.28.0"], check=True)
        print("✅ Streamlit instalado")
    
    try:
        import pandas
        print("✅ Pandas - OK")
    except ImportError:
        print("❌ Pandas não encontrado - Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pandas==2.0.3"], check=True)
        print("✅ Pandas instalado")
    
    try:
        import mysql.connector
        print("✅ MySQL Connector - OK")
    except ImportError:
        print("❌ MySQL Connector não encontrado - Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "mysql-connector-python==8.2.0"], check=True)
        print("✅ MySQL Connector instalado")

def create_placeholder_files():
    """Criar arquivos placeholder para evitar erros"""
    print("\n📄 Criando arquivos placeholder...")
    
    # Arquivo de logo placeholder (vazio, mas existe)
    logo_path = "assets/logo.png"
    if not os.path.exists(logo_path):
        try:
            with open(logo_path, "w") as f:
                f.write("")
            print("✅ Placeholder de logo criado")
        except Exception as e:
            print(f"❌ Erro ao criar placeholder de logo: {e}")
    
    # Arquivo de avatar padrão
    avatar_path = "assets/default_avatar.png"
    if not os.path.exists(avatar_path):
        try:
            with open(avatar_path, "w") as f:
                f.write("")
            print("✅ Placeholder de avatar criado")
        except Exception as e:
            print(f"❌ Erro ao criar placeholder de avatar: {e}")

def test_system():
    """Testar se o sistema funciona"""
    print("\n🧪 Testando sistema...")
    
    try:
        # Testar importação dos módulos principais
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from config.database import Database
        print("✅ Módulo database - OK")
        
        from utils.helpers import setup_page_config
        print("✅ Módulo helpers - OK")
        
        from pages import dashboard
        print("✅ Módulo dashboard - OK")
        
        print("✅ Todos os módulos principais funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar sistema: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("    CORREÇÃO DE ERROS UT-SOCIOS")
    print("=" * 60)
    print()
    
    # Executar correções
    create_missing_directories()
    create_env_file()
    create_streamlit_config()
    fix_import_errors()
    create_placeholder_files()
    
    # Testar sistema
    if test_system():
        print("\n🎉 CORREÇÕES CONCLUÍDAS COM SUCESSO!")
        print("💡 Agora você pode executar: python run.py")
    else:
        print("\n⚠️ Ainda há problemas. Execute: python diagnostico.py")
    
    print("\n" + "=" * 60)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Correção cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
