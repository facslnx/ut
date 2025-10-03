# 🚀 **Como Instalar o UT-SOCIOS - Guia Completo**

## 📋 **Pré-requisitos**

- **Python 3.8+** instalado
- **MySQL** instalado e rodando
- **Windows, Linux ou Mac**

## 🎯 **Instalação Automática (Recomendada)**

### **Windows:**
```bash
# Duplo clique no arquivo ou execute no terminal:
instalacao.bat
```

### **Linux/Mac:**
```bash
# Dar permissão de execução e executar:
chmod +x instalacao.sh
./instalacao.sh
```

### **Qualquer Sistema (Python):**
```bash
# Execute o script Python:
python instalacao.py
```

## 🔧 **Instalação Manual (Se a automática falhar)**

### **1. Verificar Python**
```bash
python --version
# Deve ser 3.8 ou superior
```

### **2. Atualizar pip**
```bash
python -m pip install --upgrade pip
```

### **3. Instalar Dependências**
```bash
# Instalar em ordem específica para evitar conflitos:
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install streamlit==1.28.0
pip install mysql-connector-python==8.2.0
pip install python-dotenv==1.0.0
pip install bcrypt==4.0.1
pip install Pillow==10.1.0
pip install plotly==5.17.0
```

### **4. Verificar Instalação**
```bash
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import pandas; print('✅ Pandas OK')"
python -c "import mysql.connector; print('✅ MySQL OK')"
```

## ⚙️ **Configuração do Banco de Dados**

### **1. Configurar .env**
```bash
# Copiar arquivo de exemplo:
copy env.example .env

# Editar .env com suas configurações:
# DB_HOST=localhost
# DB_NAME=ut_socios
# DB_USER=root
# DB_PASSWORD=sua_senha
```

### **2. Configurar Banco MySQL**
```bash
# Executar script de configuração:
python setup_database.py
```

### **3. Testar Conexão**
```bash
# Verificar se tudo está funcionando:
python test_connection.py
```

## 🚀 **Executar o Sistema**

### **Opção 1: Script de Execução**
```bash
python run.py
```

### **Opção 2: Comando Direto**
```bash
streamlit run main.py
```

### **Acessar no Navegador**
```
http://localhost:8501
```

## 🔐 **Login Padrão**

- **Email:** fernando@f5desenvolve.com.br
- **Senha:** 123

## 🐛 **Solução de Problemas**

### **Erro: "ModuleNotFoundError"**
```bash
# Reinstalar dependências:
pip install -r requirements.txt
```

### **Erro: "numpy.dtype size changed"**
```bash
# Desinstalar e reinstalar:
pip uninstall numpy pandas -y
pip install numpy==1.24.3 pandas==2.0.3
```

### **Erro de Conexão com Banco**
```bash
# Verificar se MySQL está rodando
# Windows: Serviços do Windows
# Linux: sudo systemctl status mysql
# Mac: brew services list | grep mysql
```

### **Erro de Permissão (Linux/Mac)**
```bash
# Dar permissão de execução:
chmod +x instalacao.sh
chmod +x run.py
```

## 📱 **Deploy para Produção**

### **Streamlit Cloud (Gratuito)**
1. Fazer push para GitHub
2. Conectar no [Streamlit Cloud](https://streamlit.io/cloud)
3. Configurar variáveis de ambiente
4. Deploy automático

### **VPS/Servidor**
```bash
# Instalar dependências no servidor:
pip install -r requirements.txt

# Executar em background:
nohup streamlit run main.py --server.port 8501 --server.headless true &
```

## 🔍 **Verificação Final**

### **Checklist de Instalação:**
- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas sem erro
- [ ] Arquivo .env configurado
- [ ] Banco MySQL configurado
- [ ] Teste de conexão OK
- [ ] Sistema executando em http://localhost:8501
- [ ] Login funcionando

### **Comandos de Verificação:**
```bash
# Verificar Python
python --version

# Verificar dependências
python -c "import streamlit, pandas, mysql.connector; print('✅ Tudo OK')"

# Testar conexão
python test_connection.py

# Executar sistema
python run.py
```

## 🆘 **Suporte**

Se ainda tiver problemas:

1. **Verifique os logs** no terminal
2. **Confirme as versões** do Python e pip
3. **Teste a conexão** com MySQL
4. **Execute os scripts** de verificação
5. **Consulte a documentação** do Streamlit

---

**🎉 Pronto! Seu sistema UT-SOCIOS está funcionando!**

Para dúvidas específicas, consulte os arquivos:
- `README.md` - Documentação principal
- `INSTALACAO.md` - Guia detalhado
- `USO.md` - Como usar o sistema
