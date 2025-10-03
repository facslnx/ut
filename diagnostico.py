#!/usr/bin/env python3
"""
Script de Diagnóstico - UT-SOCIOS
Identifica e resolve problemas de execução
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Verificar versão do Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Versão muito antiga!")
        print("💡 Instale Python 3.8+ primeiro")
        return False

def check_dependencies():
    """Verificar dependências instaladas"""
    print("\n📦 Verificando dependências...")
    
    dependencies = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("mysql.connector", "MySQL Connector"),
        ("dotenv", "Python-dotenv"),
        ("bcrypt", "bcrypt"),
        ("PIL", "Pillow"),
        ("plotly", "Plotly")
    ]
    
    all_ok = True
    
    for module, name in dependencies:
        try:
            importlib.import_module(module)
            print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - ERRO: {e}")
            all_ok = False
    
    return all_ok

def check_files():
    """Verificar arquivos necessários"""
    print("\n📁 Verificando arquivos...")
    
    required_files = [
        "main.py",
        "config/database.py",
        "utils/helpers.py",
        "pages/dashboard.py",
        "pages/socios.py",
        "pages/comandos.py",
        "pages/faturas.py",
        "pages/usuarios.py",
        "requirements.txt"
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - OK")
        else:
            print(f"❌ {file_path} - AUSENTE")
            all_ok = False
    
    return all_ok

def check_database_config():
    """Verificar configuração do banco"""
    print("\n🗄️ Verificando configuração do banco...")
    
    if os.path.exists(".env"):
        print("✅ Arquivo .env - OK")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            host = os.getenv('DB_HOST', 'localhost')
            database = os.getenv('DB_NAME', 'ut_socios')
            user = os.getenv('DB_USER', 'root')
            password = os.getenv('DB_PASSWORD', '')
            
            print(f"   Host: {host}")
            print(f"   Database: {database}")
            print(f"   User: {user}")
            print(f"   Password: {'*' * len(password) if password else 'NÃO DEFINIDA'}")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar .env: {e}")
            return False
    else:
        print("❌ Arquivo .env - AUSENTE")
        print("💡 Execute: copy env.example .env")
        return False

def test_database_connection():
    """Testar conexão com banco"""
    print("\n🔌 Testando conexão com banco...")
    
    try:
        from config.database import Database
        db = Database()
        
        if db.connect():
            print("✅ Conexão com banco - OK")
            
            # Testar query simples
            result = db.execute_query_one("SELECT 1 as test")
            if result:
                print("✅ Query de teste - OK")
            
            db.disconnect()
            return True
        else:
            print("❌ Conexão com banco - ERRO")
            return False
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def fix_common_issues():
    """Corrigir problemas comuns"""
    print("\n🔧 Corrigindo problemas comuns...")
    
    # Criar arquivo .env se não existir
    if not os.path.exists(".env") and os.path.exists("env.example"):
        try:
            with open("env.example", "r") as src:
                content = src.read()
            with open(".env", "w") as dst:
                dst.write(content)
            print("✅ Arquivo .env criado")
        except Exception as e:
            print(f"❌ Erro ao criar .env: {e}")
    
    # Verificar se as pastas existem
    folders = ["config", "utils", "pages", ".streamlit"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Pasta {folder} criada")

def install_missing_dependencies():
    """Instalar dependências ausentes"""
    print("\n📦 Instalando dependências ausentes...")
    
    try:
        # Atualizar pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ pip atualizado")
        
        # Instalar dependências
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependências instaladas")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("    DIAGNÓSTICO UT-SOCIOS")
    print("=" * 60)
    print()
    
    # Verificações
    python_ok = check_python_version()
    files_ok = check_files()
    deps_ok = check_dependencies()
    config_ok = check_database_config()
    db_ok = test_database_connection() if config_ok else False
    
    # Resumo
    print("\n" + "=" * 60)
    print("    RESUMO DO DIAGNÓSTICO")
    print("=" * 60)
    
    checks = [
        ("Python", python_ok),
        ("Arquivos", files_ok),
        ("Dependências", deps_ok),
        ("Configuração", config_ok),
        ("Banco de Dados", db_ok)
    ]
    
    all_ok = True
    for name, status in checks:
        status_text = "✅ OK" if status else "❌ ERRO"
        print(f"{name:15} {status_text}")
        if not status:
            all_ok = False
    
    print()
    
    if all_ok:
        print("🎉 TUDO OK! Sistema pronto para uso!")
        print("💡 Execute: python run.py")
    else:
        print("⚠️ PROBLEMAS ENCONTRADOS!")
        print()
        
        # Corrigir problemas
        fix_common_issues()
        
        if not deps_ok:
            print("💡 Tentando instalar dependências...")
            install_missing_dependencies()
        
        if not config_ok:
            print("💡 Configure o arquivo .env com suas credenciais de banco")
        
        if not db_ok:
            print("💡 Verifique se o MySQL está rodando e as credenciais estão corretas")
        
        print("\n🔄 Execute o diagnóstico novamente após corrigir os problemas")
    
    print("\n" + "=" * 60)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Diagnóstico cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
