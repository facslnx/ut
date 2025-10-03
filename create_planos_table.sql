-- Criar tabela de planos
CREATE TABLE IF NOT EXISTS planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    valor DECIMAL(10,2) NOT NULL,
    periodicidade ENUM('Mensal', 'Trimestral', 'Anual') NOT NULL,
    desconto_loja INT NOT NULL DEFAULT 0,
    desconto_caravanas INT NOT NULL DEFAULT 0,
    desconto_bar INT NOT NULL DEFAULT 0,
    inclui_camisa BOOLEAN DEFAULT FALSE,
    camisa_tipo VARCHAR(50),
    sorteio_mensal BOOLEAN DEFAULT FALSE,
    grupo_exclusivo BOOLEAN DEFAULT TRUE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Inserir os planos padrão
INSERT INTO planos (nome, descricao, valor, periodicidade, desconto_loja, desconto_caravanas, desconto_bar, inclui_camisa, camisa_tipo, sorteio_mensal, grupo_exclusivo, ativo) VALUES
('Sócio União Bronze 🥉', 'Plano básico com benefícios essenciais', 50.00, 'Trimestral', 10, 10, 0, FALSE, NULL, FALSE, TRUE, TRUE),
('Sócio União Prata 🥈', 'Plano intermediário com mais benefícios', 250.00, 'Anual', 20, 20, 0, TRUE, 'Sócio União', FALSE, TRUE, TRUE),
('Sócio União Ouro 🥇', 'Plano premium com todos os benefícios', 100.00, 'Mensal', 40, 40, 10, TRUE, 'Exclusiva Sócio Ouro', TRUE, TRUE, TRUE);

-- Adicionar coluna plano_id na tabela socios (se não existir)
ALTER TABLE socios ADD COLUMN IF NOT EXISTS plano_id INT NULL;
ALTER TABLE socios ADD FOREIGN KEY IF NOT EXISTS (plano_id) REFERENCES planos(id);

-- Adicionar coluna data_adesao_plano na tabela socios
ALTER TABLE socios ADD COLUMN IF NOT EXISTS data_adesao_plano DATE NULL;

-- Adicionar coluna data_vencimento_plano na tabela socios
ALTER TABLE socios ADD COLUMN IF NOT EXISTS data_vencimento_plano DATE NULL;

