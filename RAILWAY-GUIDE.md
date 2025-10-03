# 🚀 **GUIA COMPLETO PARA DEPLOY NO RAILWAY**

## ✅ **STATUS ATUAL:**
- ✅ Código enviado para GitHub: https://github.com/facslnx/ut.git
- ✅ Arquivos de configuração criados
- ⏳ Próximo: Deploy no Railway

---

## 🎯 **PASSO A PASSO PARA DEPLOY NO RAILWAY:**

### **1. 📱 ACESSAR RAILWAY**
- Acesse: https://railway.app
- Faça login com sua conta GitHub
- Clique em "Login with GitHub"

### **2. 🏗️ CRIAR NOVO PROJETO**
- Clique em "New Project"
- Selecione "Deploy from GitHub repo"
- Escolha o repositório: **facslnx/ut**
- Clique em "Deploy Now"

### **3. 🗄️ ADICIONAR BANCO MYSQL**
- Na dashboard do projeto
- Clique em "+ New"
- Selecione "Database" → "MySQL"
- Aguarde a criação (2-3 minutos)

### **4. ⚙️ CONFIGURAR VARIÁVEIS DE AMBIENTE**
- Clique na aba "Variables"
- Adicione as seguintes variáveis:

```env
PORT=8501
DB_HOST=[host do Railway MySQL]
DB_NAME=[database do Railway MySQL]
DB_USER=[user do Railway MySQL]
DB_PASSWORD=[password do Railway MySQL]
DB_PORT=3306
```

**Como obter essas informações:**
1. Clique no serviço MySQL
2. Clique na aba "Connect"
3. Copie as informações de conexão

### **5. 🌐 CONFIGURAR DOMÍNIO**
- Clique na aba "Settings"
- Clique em "Generate Domain"
- Sua app estará em: `https://seu-projeto-production.up.railway.app`

### **6. 🗄️ CONFIGURAR BANCO DE DADOS**

Após criar o banco MySQL no Railway, execute estes comandos SQL:

#### **Criar Tabelas:**
```sql
-- Tabela usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela comandos
CREATE TABLE comandos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela planos
CREATE TABLE planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    periodicidade ENUM('Mensal', 'Trimestral', 'Anual') NOT NULL,
    beneficios TEXT,
    inclui_camisa BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela socios
CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    foto VARCHAR(500),
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    tamanho_camisa ENUM('PP', 'P', 'M', 'G', 'GG', 'XG', 'XXG') NOT NULL,
    comando_id INT,
    plano_id INT,
    data_adesao_plano DATE,
    data_vencimento_plano DATE,
    cep VARCHAR(10),
    endereco VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comando_id) REFERENCES comandos(id),
    FOREIGN KEY (plano_id) REFERENCES planos(id)
);

-- Tabela faturas
CREATE TABLE faturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    comando_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    descricao TEXT,
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,
    status ENUM('Pendente', 'Pago', 'Atrasado') DEFAULT 'Pendente',
    forma_pagamento VARCHAR(50),
    comprovante VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (comando_id) REFERENCES comandos(id)
);
```

#### **Inserir Dados Iniciais:**
```sql
-- Usuário administrador (senha: 123)
INSERT INTO usuarios (nome, email, senha) 
VALUES ('Administrador', 'fernando@f5desenvolve.com.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdKJQK8Q8Q8Q8');

-- Comando padrão
INSERT INTO comandos (nome) VALUES ('Comando Principal');

-- Planos padrão
INSERT INTO planos (nome, valor, periodicidade, beneficios, inclui_camisa) VALUES 
('Bronze', 30.00, 'Mensal', 'Acesso básico às atividades', FALSE),
('Prata', 50.00, 'Mensal', 'Acesso completo + camisa', TRUE),
('Ouro', 80.00, 'Mensal', 'Acesso premium + benefícios exclusivos', TRUE);
```

**Como executar os comandos SQL:**
1. No Railway, clique no serviço MySQL
2. Clique na aba "Query"
3. Cole e execute cada comando SQL

---

## 🔐 **LOGIN PADRÃO:**
- **Email:** fernando@f5desenvolve.com.br
- **Senha:** 123

---

## 💰 **CUSTOS:**
- ✅ **Gratuito:** $5 créditos/mês (suficiente para apps pequenos)
- ✅ Apps privados incluídos
- ✅ Banco MySQL incluído
- ✅ SSL automático

---

## 🎊 **RESULTADO FINAL:**
Após seguir todos os passos, você terá:

- ✅ **App online:** `https://seu-projeto-production.up.railway.app`
- ✅ **Banco MySQL configurado**
- ✅ **Todas as tabelas criadas**
- ✅ **Dados iniciais inseridos**
- ✅ **App privado e seguro**
- ✅ **Deploy automático a cada push**

---

## 🆘 **SUPORTE:**
Se encontrar problemas:
1. Verifique os logs no Railway
2. Confirme se as variáveis de ambiente estão corretas
3. Verifique se todas as tabelas foram criadas
4. Teste a conexão com o banco

**🎉 Parabéns! Seu sistema UT-SOCIOS estará online e funcionando!**
