# 🔧 **Correção Rápida de Erros - UT-SOCIOS**

## ❌ **Erro: MediaFileStorageError: Error opening 'assets/logo.png'**

### **🚀 Solução Rápida (1 comando):**
```bash
python corrigir_erros.py
```

### **🔧 Solução Manual:**

#### **1. Criar diretórios necessários:**
```bash
mkdir assets
mkdir uploads
mkdir uploads\comprovantes
mkdir .streamlit
```

#### **2. Criar arquivos placeholder:**
```bash
echo. > assets\logo.png
echo. > assets\default_avatar.png
```

#### **3. Executar sistema:**
```bash
python run.py
```

## 🐛 **Outros Erros Comuns**

### **Erro: ModuleNotFoundError**
```bash
# Instalar dependências:
python instalacao.py
```

### **Erro: numpy.dtype size changed**
```bash
# Reinstalar NumPy e Pandas:
pip uninstall numpy pandas -y
pip install numpy==1.24.3 pandas==2.0.3
```

### **Erro: Connection refused (MySQL)**
```bash
# Verificar se MySQL está rodando
# Windows: Serviços do Windows
# Linux: sudo systemctl start mysql
# Mac: brew services start mysql
```

### **Erro: Permission denied**
```bash
# Dar permissão de execução (Linux/Mac):
chmod +x instalacao.sh
chmod +x run.py
```

## 🚀 **Scripts de Correção Disponíveis**

### **1. Correção Automática:**
```bash
python corrigir_erros.py
```

### **2. Diagnóstico Completo:**
```bash
python diagnostico.py
```

### **3. Instalação Completa:**
```bash
python instalacao.py
```

### **4. Execução com Verificações:**
```bash
python run.py
```

## ✅ **Verificação Final**

### **Checklist de Correção:**
- [ ] Diretórios criados (assets, uploads, .streamlit)
- [ ] Arquivos placeholder criados
- [ ] Dependências instaladas
- [ ] Arquivo .env configurado
- [ ] MySQL rodando
- [ ] Sistema executando sem erros

### **Comandos de Verificação:**
```bash
# Verificar estrutura:
dir assets
dir uploads
dir .streamlit

# Verificar dependências:
python -c "import streamlit, pandas, mysql.connector; print('OK')"

# Testar sistema:
python run.py
```

## 🆘 **Se Ainda Der Erro**

### **1. Execute o diagnóstico:**
```bash
python diagnostico.py
```

### **2. Execute a correção:**
```bash
python corrigir_erros.py
```

### **3. Reinstale tudo:**
```bash
python instalacao.py
```

### **4. Execute com verificações:**
```bash
python run.py
```

## 📱 **Acesso ao Sistema**

Após corrigir os erros:
- **URL:** http://localhost:8501
- **Login:** fernando@f5desenvolve.com.br
- **Senha:** 123

---

**🎉 Problemas resolvidos! Sistema funcionando!**
