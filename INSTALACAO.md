# 🚀 Guia de Instalação - UT-SOCIOS Streamlit

## 📋 Pré-requisitos

- **Python 3.8+** instalado
- **MySQL 5.7+** instalado e rodando
- **Git** (opcional, para clonar o repositório)

## 🔧 Instalação Passo a Passo

### 1. **Preparar o Ambiente**

```bash
# Verificar versão do Python
python --version

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. **Instalar Dependências**

```bash
# Instalar pacotes necessários
pip install -r requirements.txt
```

### 3. **Configurar Banco de Dados**

```bash
# Copiar arquivo de configuração
copy env.example .env

# Editar arquivo .env com suas configurações
# DB_HOST=localhost
# DB_NAME=ut_socios
# DB_USER=root
# DB_PASSWORD=sua_senha
```

### 4. **Configurar Banco MySQL**

```bash
# Executar script de configuração
python setup_database.py
```

### 5. **Executar o Sistema**

```bash
# Opção 1: Script de execução
python run.py

# Opção 2: Comando direto
streamlit run main.py
```

### 6. **Acessar o Sistema**

Abra seu navegador e acesse:
```
http://localhost:8501
```

## 🔐 Login Padrão

- **Email:** fernando@f5desenvolve.com.br
- **Senha:** 123

## 🐛 Solução de Problemas

### Erro de Conexão com Banco
```bash
# Verificar se MySQL está rodando
# Windows: Serviços do Windows
# Linux: sudo systemctl status mysql
# Mac: brew services list | grep mysql
```

### Erro de Dependências
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Erro de Porta
```bash
# Usar porta diferente
streamlit run main.py --server.port 8502
```

## 📱 Deploy para Produção

### Streamlit Cloud (Gratuito)
1. Fazer push para GitHub
2. Conectar no [Streamlit Cloud](https://streamlit.io/cloud)
3. Configurar variáveis de ambiente
4. Deploy automático

### VPS/Servidor
1. Instalar Python e MySQL no servidor
2. Configurar banco de dados
3. Executar: `streamlit run main.py --server.port 8501 --server.headless true`

## 🔧 Configurações Avançadas

### Personalizar Tema
Editar arquivo `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#ff0000"
backgroundColor = "#000000"
secondaryBackgroundColor = "#1a1a1a"
textColor = "#ffffff"
```

### Configurar Banco Externo
Editar arquivo `.env`:
```env
DB_HOST=seu-servidor.com
DB_NAME=ut_socios
DB_USER=usuario
DB_PASSWORD=senha_forte
```

## 📊 Estrutura do Banco

O sistema criará automaticamente:
- ✅ Tabela `usuarios`
- ✅ Tabela `comandos`
- ✅ Tabela `socios`
- ✅ Tabela `faturas`
- ✅ Usuário padrão
- ✅ Comandos de exemplo

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Confirme a conexão com MySQL
3. Verifique as dependências instaladas
4. Consulte a documentação do Streamlit

---

**🎉 Pronto! Seu sistema UT-SOCIOS está funcionando!**
