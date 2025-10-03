#!/usr/bin/env python3
"""
Script para criar a tabela de planos e inserir os dados padrão
"""

from config.database import db

def create_planos_table():
    """Criar tabela de planos e inserir dados padrão"""
    
    # Conectar ao banco
    if not db.connect():
        print("[ERRO] Erro ao conectar com o banco de dados")
        return False
    
    try:
        # Criar tabela de planos
        create_table_sql = """
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
        )
        """
        
        if db.execute_query(create_table_sql):
            print("[OK] Tabela 'planos' criada com sucesso")
        else:
            print("[ERRO] Erro ao criar tabela 'planos'")
            return False
        
        # Verificar se já existem planos
        check_planos = db.execute_query("SELECT COUNT(*) as total FROM planos", fetch=True)
        if check_planos and check_planos[0]['total'] > 0:
            print("[INFO] Planos já existem no banco")
            return True
        
        # Inserir planos padrão
        planos_data = [
            {
                'nome': 'Socio Uniao Bronze',
                'descricao': 'Plano basico com beneficios essenciais',
                'valor': 50.00,
                'periodicidade': 'Trimestral',
                'desconto_loja': 10,
                'desconto_caravanas': 10,
                'desconto_bar': 0,
                'inclui_camisa': False,
                'camisa_tipo': None,
                'sorteio_mensal': False,
                'grupo_exclusivo': True
            },
            {
                'nome': 'Socio Uniao Prata',
                'descricao': 'Plano intermediario com mais beneficios',
                'valor': 250.00,
                'periodicidade': 'Anual',
                'desconto_loja': 20,
                'desconto_caravanas': 20,
                'desconto_bar': 0,
                'inclui_camisa': True,
                'camisa_tipo': 'Socio Uniao',
                'sorteio_mensal': False,
                'grupo_exclusivo': True
            },
            {
                'nome': 'Socio Uniao Ouro',
                'descricao': 'Plano premium com todos os beneficios',
                'valor': 100.00,
                'periodicidade': 'Mensal',
                'desconto_loja': 40,
                'desconto_caravanas': 40,
                'desconto_bar': 10,
                'inclui_camisa': True,
                'camisa_tipo': 'Exclusiva Socio Ouro',
                'sorteio_mensal': True,
                'grupo_exclusivo': True
            }
        ]
        
        insert_sql = """
        INSERT INTO planos (nome, descricao, valor, periodicidade, desconto_loja, 
                           desconto_caravanas, desconto_bar, inclui_camisa, camisa_tipo, 
                           sorteio_mensal, grupo_exclusivo, ativo)
        VALUES (%(nome)s, %(descricao)s, %(valor)s, %(periodicidade)s, %(desconto_loja)s,
                %(desconto_caravanas)s, %(desconto_bar)s, %(inclui_camisa)s, %(camisa_tipo)s,
                %(sorteio_mensal)s, %(grupo_exclusivo)s, TRUE)
        """
        
        for plano in planos_data:
            if db.execute_query(insert_sql, plano):
                print(f"[OK] Plano '{plano['nome']}' inserido com sucesso")
            else:
                print(f"[ERRO] Erro ao inserir plano '{plano['nome']}'")
        
        # Adicionar colunas na tabela socios se não existirem
        alter_socios_sql = [
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS plano_id INT NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS data_adesao_plano DATE NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS data_vencimento_plano DATE NULL"
        ]
        
        for sql in alter_socios_sql:
            try:
                db.execute_query(sql)
                print(f"[OK] Coluna adicionada: {sql.split()[-1]}")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"[INFO] Coluna já existe: {sql.split()[-1]}")
                else:
                    print(f"[ERRO]: {e}")
        
        # Adicionar foreign key se não existir
        try:
            fk_sql = "ALTER TABLE socios ADD FOREIGN KEY (plano_id) REFERENCES planos(id)"
            db.execute_query(fk_sql)
            print("[OK] Foreign key adicionada")
        except Exception as e:
            if "Duplicate key name" in str(e) or "already exists" in str(e):
                print("[INFO] Foreign key já existe")
            else:
                print(f"[ERRO] Erro ao adicionar foreign key: {e}")
        
        print("\n[SUCESSO] Sistema de planos configurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro geral: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("Configurando sistema de planos...")
    print("=" * 50)
    create_planos_table()
