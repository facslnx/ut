# 🚀 UT-SOCIOS - Guia de Deploy Completo

Sistema de Gestão de Sócios da União Tricolor - Deploy Automático no Railway

## 📋 Scripts Disponíveis

### 🎯 Script Principal
```bash
python deploy-ut-socios.py
```
**Script principal que orquestra todo o processo de deploy**

### 🔧 Scripts Individuais

#### 1. Configuração Git + GitHub
```bash
python git-install.py
```
**Configura Git, faz upload para GitHub e prepara para Railway**

#### 2. Correção de Problemas Git
```bash
python git-fix.py
```
**Corrige problemas específicos do Git (autenticação, remote, etc.)**

#### 3. Configuração do Banco
```bash
python railway-setup.py
```
**Configura banco MySQL no Railway e cria tabelas**

## 🎯 Processo Completo

### **OPÇÃO 1: Deploy Automático (Recomendado)**
```bash
python deploy-ut-socios.py
```
- Escolha opção 4: "Deploy completo"
- Siga as instruções na tela
- Tudo será feito automaticamente

### **OPÇÃO 2: Deploy Manual**
```bash
# 1. Configurar Git e GitHub
python git-install.py

# 2. Configurar banco de dados
python railway-setup.py

# 3. Fazer deploy no Railway (manual)
```

## 🔧 Pré-requisitos

### ✅ Obrigatórios
- [x] Python 3.8+ instalado
- [x] Streamlit instalado (`pip install streamlit`)
- [x] Conta no GitHub
- [x] Conta no Railway

### 📁 Estrutura do Projeto
```
UT-SOCIOS/
├── main.py                    # ✅ App principal
├── requirements.txt           # ✅ Dependências
├── config/database.py         # ✅ Conexão DB
├── pages/                     # ✅ Páginas do app
├── utils/                     # ✅ Utilitários
├── assets/                    # ✅ Arquivos estáticos
├── deploy-ut-socios.py        # 🆕 Script principal
├── git-install.py            # 🆕 Configuração Git
├── git-fix.py                # 🆕 Correção Git
└── railway-setup.py          # 🆕 Configuração DB
```

## 🚀 Deploy no Railway

### **PASSO 1: Preparar Projeto**
```bash
# No diretório do projeto
python deploy-ut-socios.py
```

### **PASSO 2: Criar Repositório GitHub**
1. Acesse: https://github.com/new
2. Nome: `ut-socios-streamlit`
3. Visibilidade: **Private** (recomendado)
4. **NÃO** marque "Add README"
5. Clique "Create repository"

### **PASSO 3: Deploy no Railway**
1. Acesse: https://railway.app
2. Login com GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Escolha seu repositório
5. Clique "Deploy Now"

### **PASSO 4: Configurar Banco MySQL**
1. Na dashboard: "+ New" → "Database" → "MySQL"
2. Aguarde criação (2-3 minutos)
3. Use `railway-setup.py` para configurar

### **PASSO 5: Configurar Variáveis**
```env
PORT=8501
DB_HOST=[host do Railway]
DB_NAME=[database do Railway]
DB_USER=[user do Railway]
DB_PASSWORD=[password do Railway]
DB_PORT=[port do Railway]
```

### **PASSO 6: Configurar Domínio**
1. Settings → Generate Domain
2. Sua app: `https://seu-projeto-production.up.railway.app`

## 🔐 Login Padrão

- **Email:** fernando@f5desenvolve.com.br
- **Senha:** 123

## 💰 Custos

### **Railway Gratuito**
- ✅ $5 créditos/mês (suficiente para apps pequenos)
- ✅ Apps privados incluídos
- ✅ Banco MySQL incluído
- ✅ SSL automático

### **Upgrade (se necessário)**
- Pro: $5/mês por desenvolvedor
- Team: $20/mês por desenvolvedor

## 🚨 Solução de Problemas

### **❌ Erro no Git Push**
```bash
python git-fix.py
```
- Configura autenticação
- Corrige problemas de remote
- Reconfigura credenciais

### **❌ Erro de Conexão com Banco**
1. Verifique variáveis de ambiente no Railway
2. Confirme se banco MySQL foi criado
3. Execute `railway-setup.py` novamente

### **❌ App não carrega**
1. Verifique logs no Railway
2. Confirme se `main.py` está na raiz
3. Verifique se dependências estão no `requirements.txt`

### **❌ Erro de Importação**
1. Confirme se todos os arquivos estão no repositório
2. Verifique se `.gitignore` não está ignorando arquivos necessários

## 📞 Suporte

### **Scripts de Diagnóstico**
```bash
# Verificar problemas Git
python git-fix.py

# Reconfigurar banco
python railway-setup.py

# Deploy completo
python deploy-ut-socios.py
```

### **Logs do Railway**
1. Dashboard → Sua app → Logs
2. Verifique erros de conexão
3. Confirme variáveis de ambiente

### **Teste Local**
```bash
# Testar antes do deploy
streamlit run main.py

# Verificar dependências
pip install -r requirements.txt
```

## 🎊 Resultado Final

Após o deploy bem-sucedido, você terá:

### **🌐 App Online**
- URL: `https://seu-projeto-production.up.railway.app`
- SSL automático
- Deploy automático a cada push

### **🔒 Segurança**
- App privado (código não público)
- Banco de dados hospedado
- Autenticação segura

### **⚡ Performance**
- Cache otimizado
- Deploy rápido
- Logs em tempo real

### **📱 Funcionalidades**
- ✅ Dashboard completo
- ✅ Gestão de sócios
- ✅ Upload de fotos
- ✅ Relatórios e gráficos
- ✅ Sistema de planos
- ✅ Gestão financeira

## 🎯 Próximos Passos

### **Melhorias Futuras**
1. **Custom Domain** (pago)
2. **Backup automático** do banco
3. **Monitoramento** avançado
4. **CI/CD** personalizado

### **Manutenção**
1. **Atualizações** via GitHub push
2. **Backup** regular do banco
3. **Monitoramento** de logs
4. **Otimizações** de performance

---

**🎉 Parabéns! Seu sistema UT-SOCIOS está online e funcionando!**

**Desenvolvido com ❤️ para a União Tricolor**
