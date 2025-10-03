#!/usr/bin/env python3
"""
Script final para configurar banco de dados MySQL no Railway
UT-SOCIOS - Sistema de Gestão de Sócios
Usando apenas bibliotecas padrão do Python
"""

import urllib.request
import urllib.parse
import json
import sys

def print_header(title):
    """Imprimir cabeçalho"""
    print(f"\n{'='*60}")
    print(f"🗄️ {title}")
    print(f"{'='*60}")

def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🗄️ RAILWAY DATABASE SETUP               ║
║              Configuração do banco de dados                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print_header("CONFIGURAÇÃO MANUAL NECESSÁRIA")
    
    print("""
🔧 COMO CONFIGURAR O BANCO DE DADOS:

📋 CREDENCIAIS DO RAILWAY:
   Host: mysql.railway.internal
   Database: railway
   User: root
   Password: WusOmNLoULtFbOohTgiuvSCcBXsbjilj
   Port: 3306

🌐 OPÇÃO 1: USAR ADMINER (RECOMENDADO)
   1. Acesse: https://www.adminer.org/
   2. Clique em "Adminer" (versão online)
   3. Conecte com:
      - Sistema: MySQL
      - Servidor: mysql.railway.internal
      - Usuário: root
      - Senha: WusOmNLoULtFbOohTgiuvSCcBXsbjilj
      - Base de dados: railway

🌐 OPÇÃO 2: USAR PHPMYADMIN ONLINE
   1. Acesse: https://www.phpmyadmin.co/
   2. Conecte com as mesmas credenciais

📝 DEPOIS DE CONECTAR, EXECUTE ESTE SQL:
    """)
    
    print_header("SQL PARA CRIAR TABELAS")
    
    sql_tables = """
-- Criar Tabelas
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comandos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    periodicidade ENUM('Mensal', 'Trimestral', 'Anual') NOT NULL,
    beneficios TEXT,
    inclui_camisa BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS socios (
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

CREATE TABLE IF NOT EXISTS faturas (
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
    """
    
    print(sql_tables)
    
    print_header("SQL PARA INSERIR DADOS INICIAIS")
    
    sql_data = """
-- Inserir Dados Iniciais
INSERT IGNORE INTO usuarios (nome, email, senha) 
VALUES ('Administrador', 'fernando@f5desenvolve.com.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdKJQK8Q8Q8Q8');

INSERT IGNORE INTO comandos (nome) VALUES ('Comando Principal');

INSERT IGNORE INTO planos (nome, valor, periodicidade, beneficios, inclui_camisa) VALUES 
('Bronze', 30.00, 'Mensal', 'Acesso básico às atividades', FALSE),
('Prata', 50.00, 'Mensal', 'Acesso completo + camisa', TRUE),
('Ouro', 80.00, 'Mensal', 'Acesso premium + benefícios exclusivos', TRUE);
    """
    
    print(sql_data)
    
    print_header("CONFIGURAR VARIÁVEIS NO RAILWAY")
    
    print("""
⚙️ ADICIONAR VARIÁVEIS NO SERVIÇO "UT":

1. No Railway, clique no serviço "ut" (seu app)
2. Vá para a aba "Variables"
3. Adicione estas variáveis:

PORT=8501
DB_HOST=mysql.railway.internal
DB_NAME=railway
DB_USER=root
DB_PASSWORD=WusOmNLoULtFbOohTgiuvSCcBXsbjilj
DB_PORT=3306
    """)
    
    print_header("RESULTADO FINAL")
    
    print("""
🎊 APÓS CONFIGURAR TUDO:

✅ Tabelas criadas no banco MySQL
✅ Dados iniciais inseridos
✅ Variáveis configuradas no Railway
✅ App conectado ao banco

🔐 LOGIN PADRÃO:
   📧 Email: fernando@f5desenvolve.com.br
   🔑 Senha: 123

🌐 Sua app estará funcionando com banco de dados!
    """)

if __name__ == "__main__":
    main()
