-- ========================================
-- UT-SOCIOS - Configuração do Supabase
-- Sistema de Gestão de Sócios - União Tricolor
-- ========================================

-- Criar Tabelas
-- ========================================

-- Tabela usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela comandos
CREATE TABLE IF NOT EXISTS comandos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela planos
CREATE TABLE IF NOT EXISTS planos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    periodicidade VARCHAR(20) NOT NULL CHECK (periodicidade IN ('Mensal', 'Trimestral', 'Anual')),
    beneficios TEXT,
    inclui_camisa BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela socios
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (comando_id) REFERENCES comandos(id),
    FOREIGN KEY (plano_id) REFERENCES planos(id)
);

-- Tabela faturas
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (comando_id) REFERENCES comandos(id)
);

-- Inserir Dados Iniciais
-- ========================================

-- Usuário administrador (senha: 123)
-- Hash bcrypt da senha "123"
INSERT INTO usuarios (nome, email, senha) 
VALUES ('Administrador', 'fernando@f5desenvolve.com.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdKJQK8Q8Q8Q8')
ON CONFLICT (email) DO NOTHING;

-- Comando padrão
INSERT INTO comandos (nome) VALUES ('Comando Principal')
ON CONFLICT DO NOTHING;

-- Planos padrão
INSERT INTO planos (nome, valor, periodicidade, beneficios, inclui_camisa) VALUES 
('Bronze', 30.00, 'Mensal', 'Acesso básico às atividades', FALSE),
('Prata', 50.00, 'Mensal', 'Acesso completo + camisa', TRUE),
('Ouro', 80.00, 'Mensal', 'Acesso premium + benefícios exclusivos', TRUE)
ON CONFLICT DO NOTHING;

-- Configurar RLS (Row Level Security) para Supabase
-- ========================================

-- Habilitar RLS nas tabelas
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE comandos ENABLE ROW LEVEL SECURITY;
ALTER TABLE planos ENABLE ROW LEVEL SECURITY;
ALTER TABLE socios ENABLE ROW LEVEL SECURITY;
ALTER TABLE faturas ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso (permitir tudo para facilitar desenvolvimento)
CREATE POLICY "Allow all operations on usuarios" ON usuarios FOR ALL USING (true);
CREATE POLICY "Allow all operations on comandos" ON comandos FOR ALL USING (true);
CREATE POLICY "Allow all operations on planos" ON planos FOR ALL USING (true);
CREATE POLICY "Allow all operations on socios" ON socios FOR ALL USING (true);
CREATE POLICY "Allow all operations on faturas" ON faturas FOR ALL USING (true);

-- Verificar se tudo foi criado
-- ========================================
SELECT 'Tabelas criadas com sucesso!' as status;

SELECT 'Usuários:' as tabela, COUNT(*) as total FROM usuarios
UNION ALL
SELECT 'Comandos:', COUNT(*) FROM comandos
UNION ALL
SELECT 'Planos:', COUNT(*) FROM planos
UNION ALL
SELECT 'Sócios:', COUNT(*) FROM socios
UNION ALL
SELECT 'Faturas:', COUNT(*) FROM faturas;
