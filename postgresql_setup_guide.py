#!/usr/bin/env python3
"""
Guia para configurar PostgreSQL no Railway
UT-SOCIOS - Sistema de Gestão de Sócios
"""

def print_header(title):
    """Imprimir cabeçalho"""
    print(f"\n{'='*60}")
    print(f"🐘 {title}")
    print(f"{'='*60}")

def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🐘 POSTGRESQL RAILWAY SETUP              ║
║              Configuração do banco de dados                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print_header("CONFIGURAR VARIÁVEIS NO RAILWAY")
    
    print("""
⚙️ ADICIONAR VARIÁVEIS NO SERVIÇO "UT":

1. No Railway, clique no serviço "ut" (seu app)
2. Vá para a aba "Variables"
3. Adicione esta variável:

DATABASE_URL=postgresql://postgres:VQPMNujhvABRENVajnwlicFmzHOXssKU@postgres.railway.internal:5432/railway

OU as variáveis individuais:
DB_HOST=postgres.railway.internal
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=VQPMNujhvABRENVajnwlicFmzHOXssKU
DB_PORT=5432
    """)
    
    print_header("CRIAR TABELAS NO POSTGRESQL")
    
    print("""
🌐 USAR ADMINER PARA POSTGRESQL:

1. Acesse: https://www.adminer.org/
2. Clique em "Adminer" (versão online)
3. Conecte com:
   - Sistema: PostgreSQL
   - Servidor: postgres.railway.internal
   - Usuário: postgres
   - Senha: VQPMNujhvABRENVajnwlicFmzHOXssKU
   - Base de dados: railway
4. Execute o SQL abaixo:
    """)
    
    sql_tables = """
-- Criar Tabelas PostgreSQL
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comandos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS planos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    periodicidade VARCHAR(20) NOT NULL CHECK (periodicidade IN ('Mensal', 'Trimestral', 'Anual')),
    beneficios TEXT,
    inclui_camisa BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS socios (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    foto VARCHAR(500),
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    tamanho_camisa VARCHAR(10) NOT NULL CHECK (tamanho_camisa IN ('PP', 'P', 'M', 'G', 'GG', 'XG', 'XXG')),
    comando_id INTEGER,
    plano_id INTEGER,
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
    id SERIAL PRIMARY KEY,
    socio_id INTEGER NOT NULL,
    comando_id INTEGER NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    descricao TEXT,
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,
    status VARCHAR(20) DEFAULT 'Pendente' CHECK (status IN ('Pendente', 'Pago', 'Atrasado')),
    forma_pagamento VARCHAR(50),
    comprovante VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (comando_id) REFERENCES comandos(id)
);
    """
    
    print(sql_tables)
    
    print_header("INSERIR DADOS INICIAIS")
    
    sql_data = """
-- Inserir Dados Iniciais
INSERT INTO usuarios (nome, email, senha) 
VALUES ('Administrador', 'fernando@f5desenvolve.com.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdKJQK8Q8Q8Q8')
ON CONFLICT (email) DO NOTHING;

INSERT INTO comandos (nome) VALUES ('Comando Principal')
ON CONFLICT DO NOTHING;

INSERT INTO planos (nome, valor, periodicidade, beneficios, inclui_camisa) VALUES 
('Bronze', 30.00, 'Mensal', 'Acesso básico às atividades', FALSE),
('Prata', 50.00, 'Mensal', 'Acesso completo + camisa', TRUE),
('Ouro', 80.00, 'Mensal', 'Acesso premium + benefícios exclusivos', TRUE)
ON CONFLICT DO NOTHING;
    """
    
    print(sql_data)
    
    print_header("RESULTADO FINAL")
    
    print("""
🎊 APÓS CONFIGURAR TUDO:

✅ Variáveis configuradas no Railway
✅ Tabelas criadas no PostgreSQL
✅ Dados iniciais inseridos
✅ App conectado ao banco

🔐 LOGIN PADRÃO:
   📧 Email: fernando@f5desenvolve.com.br
   🔑 Senha: 123

🌐 Sua app estará funcionando com PostgreSQL!
    """)

if __name__ == "__main__":
    main()
