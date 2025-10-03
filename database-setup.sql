-- ========================================
-- UT-SOCIOS - Configuração do Banco MySQL
-- Sistema de Gestão de Sócios - União Tricolor
-- ========================================

-- Criar Tabelas
-- ========================================

-- Tabela usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela comandos
CREATE TABLE IF NOT EXISTS comandos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela planos
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

-- Tabela socios
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

-- Tabela faturas
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

-- Inserir Dados Iniciais
-- ========================================

-- Usuário administrador (senha: 123)
-- Hash bcrypt da senha "123"
INSERT IGNORE INTO usuarios (nome, email, senha) 
VALUES ('Administrador', 'fernando@f5desenvolve.com.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdKJQK8Q8Q8Q8');

-- Comando padrão
INSERT IGNORE INTO comandos (nome) VALUES ('Comando Principal');

-- Planos padrão
INSERT IGNORE INTO planos (nome, valor, periodicidade, beneficios, inclui_camisa) VALUES 
('Bronze', 30.00, 'Mensal', 'Acesso básico às atividades', FALSE),
('Prata', 50.00, 'Mensal', 'Acesso completo + camisa', TRUE),
('Ouro', 80.00, 'Mensal', 'Acesso premium + benefícios exclusivos', TRUE);

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
