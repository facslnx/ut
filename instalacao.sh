#!/bin/bash

echo "========================================"
echo "    INSTALACAO AUTOMATICA UT-SOCIOS"
echo "========================================"
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERRO: Python3 não encontrado!"
    echo "💡 Instale o Python 3.8+ primeiro"
    echo "📥 Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "📥 CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "📥 Mac: brew install python3"
    exit 1
fi

echo "✅ Python encontrado!"
python3 --version
echo

# Atualizar pip
echo "🔄 Atualizando pip..."
python3 -m pip install --upgrade pip
echo

# Desinstalar pacotes problemáticos
echo "🧹 Limpando instalações anteriores..."
pip3 uninstall pandas numpy streamlit mysql-connector-python python-dotenv bcrypt -y > /dev/null 2>&1
echo

# Limpar cache
echo "🗑️ Limpando cache..."
pip3 cache purge > /dev/null 2>&1
echo

# Instalar dependências em ordem específica
echo "📦 Instalando dependências..."

echo "  - Instalando NumPy..."
pip3 install numpy==1.24.3

echo "  - Instalando Pandas..."
pip3 install pandas==2.0.3

echo "  - Instalando Streamlit..."
pip3 install streamlit==1.28.0

echo "  - Instalando MySQL Connector..."
pip3 install mysql-connector-python==8.2.0

echo "  - Instalando Python-dotenv..."
pip3 install python-dotenv==1.0.0

echo "  - Instalando bcrypt..."
pip3 install bcrypt==4.0.1

echo "  - Instalando Pillow..."
pip3 install Pillow==10.1.0

echo "  - Instalando Plotly..."
pip3 install plotly==5.17.0

echo

# Verificar instalação
echo "🔍 Verificando instalação..."

python3 -c "import numpy; print('✅ NumPy OK')" 2>/dev/null || echo "❌ NumPy ERRO"
python3 -c "import pandas; print('✅ Pandas OK')" 2>/dev/null || echo "❌ Pandas ERRO"
python3 -c "import streamlit; print('✅ Streamlit OK')" 2>/dev/null || echo "❌ Streamlit ERRO"
python3 -c "import mysql.connector; print('✅ MySQL Connector OK')" 2>/dev/null || echo "❌ MySQL Connector ERRO"
python3 -c "import dotenv; print('✅ Python-dotenv OK')" 2>/dev/null || echo "❌ Python-dotenv ERRO"
python3 -c "import bcrypt; print('✅ bcrypt OK')" 2>/dev/null || echo "❌ bcrypt ERRO"

echo

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "📝 Criando arquivo de configuração..."
    cp env.example .env
    echo "✅ Arquivo .env criado!"
    echo "💡 Edite o arquivo .env com suas configurações de banco"
else
    echo "✅ Arquivo .env já existe"
fi

echo
echo "========================================"
echo "    INSTALACAO CONCLUIDA!"
echo "========================================"
echo
echo "🚀 Próximos passos:"
echo "   1. Configure o banco de dados: python3 setup_database.py"
echo "   2. Teste a conexão: python3 test_connection.py"
echo "   3. Execute o sistema: python3 run.py"
echo
echo "🌐 Acesse: http://localhost:8501"
echo "🔐 Login: fernando@f5desenvolve.com.br / 123"
echo
