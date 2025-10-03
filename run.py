#!/usr/bin/env python3
"""
Script para executar o sistema UT-SOCIOS
"""

import subprocess
import sys
import os

def check_dependencies():
    """Verificar dependências necessárias"""
    print("🔍 Verificando dependências...")
    
    required_modules = [
        "streamlit",
        "pandas", 
        "mysql.connector",
        "dotenv",
        "bcrypt"
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - AUSENTE")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Módulos ausentes: {', '.join(missing_modules)}")
        print("💡 Execute: python instalacao.py")
        return False
    
    return True

def create_required_directories():
    """Criar diretórios necessários"""
    print("📁 Verificando diretórios...")
    
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
            print(f"✅ Pasta {directory} existe")

def create_placeholder_files():
    """Criar arquivos placeholder"""
    print("📄 Verificando arquivos placeholder...")
    
    files = [
        "assets/logo.png",
        "assets/default_avatar.png"
    ]
    
    for file_path in files:
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w") as f:
                    f.write("")
                print(f"✅ {file_path} criado")
            except Exception as e:
                print(f"⚠️ Erro ao criar {file_path}: {e}")
        else:
            print(f"✅ {file_path} existe")

def main():
    """Executar o sistema UT-SOCIOS"""
    print("=" * 50)
    print("🚀 INICIANDO UT-SOCIOS")
    print("=" * 50)
    print("📱 Sistema de Gestão de Sócios")
    print("🌐 Acesse: http://localhost:8501")
    print("🔐 Login: fernando@f5desenvolve.com.br / 123")
    print("=" * 50)
    
    try:
        # Verificar dependências
        if not check_dependencies():
            print("\n❌ Dependências ausentes!")
            print("💡 Execute: python instalacao.py")
            input("Pressione Enter para sair...")
            return
        
        # Criar diretórios necessários
        create_required_directories()
        
        # Criar arquivos placeholder
        create_placeholder_files()
        
        print("\n✅ Verificações concluídas!")
        print("🚀 Iniciando Streamlit...")
        print("=" * 50)
        
        # Executar o Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Execute: python corrigir_erros.py")
        input("Pressione Enter para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()