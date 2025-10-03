@echo off
echo ========================================
echo    INSTALACAO AUTOMATICA UT-SOCIOS
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python nao encontrado!
    echo 💡 Instale o Python 3.8+ primeiro
    echo 📥 Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version
echo.

REM Atualizar pip
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Desinstalar pacotes problemáticos
echo 🧹 Limpando instalacoes anteriores...
pip uninstall pandas numpy streamlit mysql-connector-python python-dotenv bcrypt -y >nul 2>&1
echo.

REM Limpar cache
echo 🗑️ Limpando cache...
pip cache purge >nul 2>&1
echo.

REM Instalar dependências em ordem específica
echo 📦 Instalando dependencias...

echo   - Instalando NumPy...
pip install numpy==1.24.3

echo   - Instalando Pandas...
pip install pandas==2.0.3

echo   - Instalando Streamlit...
pip install streamlit==1.28.0

echo   - Instalando MySQL Connector...
pip install mysql-connector-python==8.2.0

echo   - Instalando Python-dotenv...
pip install python-dotenv==1.0.0

echo   - Instalando bcrypt...
pip install bcrypt==4.0.1

echo   - Instalando Pillow...
pip install Pillow==10.1.0

echo   - Instalando Plotly...
pip install plotly==5.17.0

echo.

REM Criar diretórios necessários
echo 📁 Criando diretorios necessarios...
if not exist "assets" mkdir assets
if not exist "uploads" mkdir uploads
if not exist "uploads\comprovantes" mkdir uploads\comprovantes
if not exist ".streamlit" mkdir .streamlit

REM Criar arquivos placeholder
echo 📄 Criando arquivos placeholder...
echo. > assets\logo.png
echo. > assets\default_avatar.png

REM Verificar instalação
echo 🔍 Verificando instalacao...

python -c "import numpy; print('✅ NumPy OK')" 2>nul || echo ❌ NumPy ERRO
python -c "import pandas; print('✅ Pandas OK')" 2>nul || echo ❌ Pandas ERRO
python -c "import streamlit; print('✅ Streamlit OK')" 2>nul || echo ❌ Streamlit ERRO
python -c "import mysql.connector; print('✅ MySQL Connector OK')" 2>nul || echo ❌ MySQL Connector ERRO
python -c "import dotenv; print('✅ Python-dotenv OK')" 2>nul || echo ❌ Python-dotenv ERRO
python -c "import bcrypt; print('✅ bcrypt OK')" 2>nul || echo ❌ bcrypt ERRO

echo.

REM Criar arquivo .env se não existir
if not exist ".env" (
    echo 📝 Criando arquivo de configuracao...
    copy env.example .env >nul
    echo ✅ Arquivo .env criado!
    echo 💡 Edite o arquivo .env com suas configuracoes de banco
) else (
    echo ✅ Arquivo .env ja existe
)

echo.
echo ========================================
echo    INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo 🚀 Proximos passos:
echo    1. Configure o banco de dados: python setup_database.py
echo    2. Teste a conexao: python test_connection.py
echo    3. Execute o sistema: python run.py
echo.
echo 🌐 Acesse: http://localhost:8501
echo 🔐 Login: fernando@f5desenvolve.com.br / 123
echo.
pause
