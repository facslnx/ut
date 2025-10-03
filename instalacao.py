#!/usr/bin/env python3
"""
Script de Instalação Automática - UT-SOCIOS
Instala todas as dependências necessárias para o sistema
"""

import subprocess
import sys
import os
import platform

def run_command(command, description=""):
    """Executar comando e mostrar resultado"""
    if description:
        print(f"🔄 {description}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ERRO")
        if e.stderr:
            print(f"   Erro: {e.stderr}")
        return False

def check_python():
    """Verificar se Python está instalado"""
    print("🔍 Verificando Python...")
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Versão muito antiga!")
            print("💡 Instale Python 3.8+ primeiro")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar Python: {e}")
        return False

def install_packages():
    """Instalar pacotes necessários"""
    packages = [
        ("numpy==1.24.3", "NumPy"),
        ("pandas==2.0.3", "Pandas"),
        ("streamlit==1.28.0", "Streamlit"),
        ("mysql-connector-python==8.2.0", "MySQL Connector"),
        ("python-dotenv==1.0.0", "Python-dotenv"),
        ("bcrypt==4.0.1", "bcrypt"),
        ("Pillow==10.1.0", "Pillow"),
        ("plotly==5.17.0", "Plotly")
    ]
    
    print("\n📦 Instalando dependências...")
    print("=" * 50)
    
    for package, name in packages:
        if not run_command(f"pip install {package}", f"Instalando {name}"):
            print(f"⚠️  Falha ao instalar {name}, tentando continuar...")
    
    return True

def verify_installation():
    """Verificar se a instalação foi bem-sucedida"""
    print("\n🔍 Verificando instalação...")
    print("=" * 50)
    
    modules = [
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("streamlit", "Streamlit"),
        ("mysql.connector", "MySQL Connector"),
        ("dotenv", "Python-dotenv"),
        ("bcrypt", "bcrypt"),
        ("PIL", "Pillow"),
        ("plotly", "Plotly")
    ]
    
    all_ok = True
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"❌ {name} - ERRO")
            all_ok = False
    
    return all_ok

def create_env_file():
    """Criar arquivo .env se não existir"""
    print("\n📝 Configurando arquivo .env...")
    
    if os.path.exists(".env"):
        print("✅ Arquivo .env já existe")
        return True
    
    if os.path.exists("env.example"):
        try:
            with open("env.example", "r") as src:
                content = src.read()
            with open(".env", "w") as dst:
                dst.write(content)
            print("✅ Arquivo .env criado a partir do env.example")
            print("💡 Edite o arquivo .env com suas configurações de banco")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar .env: {e}")
            return False
    else:
        print("⚠️  Arquivo env.example não encontrado")
        return False

def main():
    """Função principal"""
    print("=" * 50)
    print("    INSTALAÇÃO AUTOMÁTICA UT-SOCIOS")
    print("=" * 50)
    print(f"🖥️  Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    print()
    
    # Verificar Python
    if not check_python():
        print("\n❌ Instalação cancelada!")
        input("Pressione Enter para sair...")
        return False
    
    # Atualizar pip
    print("\n🔄 Atualizando pip...")
    run_command("python -m pip install --upgrade pip", "Atualizando pip")
    
    # Limpar instalações anteriores
    print("\n🧹 Limpando instalações anteriores...")
    run_command("pip uninstall pandas numpy streamlit mysql-connector-python python-dotenv bcrypt -y", 
                "Removendo pacotes antigos")
    
    # Limpar cache
    print("\n🗑️ Limpando cache...")
    run_command("pip cache purge", "Limpando cache")
    
    # Instalar pacotes
    install_packages()
    
    # Verificar instalação
    if verify_installation():
        print("\n✅ Instalação concluída com sucesso!")
    else:
        print("\n⚠️  Instalação concluída com alguns erros")
        print("💡 Tente executar novamente ou instale manualmente os pacotes com erro")
    
    # Criar arquivo .env
    create_env_file()
    
    # Instruções finais
    print("\n" + "=" * 50)
    print("    INSTALAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print()
    print("🚀 Próximos passos:")
    print("   1. Configure o banco de dados: python setup_database.py")
    print("   2. Teste a conexão: python test_connection.py")
    print("   3. Execute o sistema: python run.py")
    print()
    print("🌐 Acesse: http://localhost:8501")
    print("🔐 Login: fernando@f5desenvolve.com.br / 123")
    print()
    
    input("Pressione Enter para sair...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
