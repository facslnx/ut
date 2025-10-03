@echo off
echo ================================================
echo 🚀 INICIANDO SISTEMA UT-SOCIOS
echo ================================================
echo 📱 Sistema de Gestão de Sócios
echo 🌐 Acesse: http://localhost:8501
echo 🔐 Login: fernando@f5desenvolve.com.br / 123
echo ================================================

REM Matar processos existentes na porta 8501
echo 🔧 Verificando portas...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    echo 🗑️ Matando processo %%a...
    taskkill /PID %%a /F >nul 2>&1
)

REM Aguardar um momento
timeout /t 2 /nobreak >nul

REM Executar o sistema
echo 🚀 Iniciando Streamlit...
python -m streamlit run main.py --server.port 8501 --server.headless true

pause
