#!/usr/bin/env python3
"""
Script para corrigir a tabela socios adicionando todas as colunas necessárias
"""

from config.database import db

def fix_socios_table():
    """Corrigir tabela socios adicionando colunas necessárias"""
    
    # Conectar ao banco
    if not db.connect():
        print("[ERRO] Erro ao conectar com o banco de dados")
        return False
    
    try:
        # Lista de alterações para fazer
        alteracoes = [
            # Campos de endereço
            "ALTER TABLE socios ADD COLUMN cep VARCHAR(10) NULL",
            "ALTER TABLE socios ADD COLUMN endereco VARCHAR(255) NULL",
            "ALTER TABLE socios ADD COLUMN numero VARCHAR(20) NULL",
            "ALTER TABLE socios ADD COLUMN complemento VARCHAR(100) NULL",
            "ALTER TABLE socios ADD COLUMN bairro VARCHAR(100) NULL",
            "ALTER TABLE socios ADD COLUMN cidade VARCHAR(100) NULL",
            "ALTER TABLE socios ADD COLUMN estado CHAR(2) NULL",
            
            # Campos de plano
            "ALTER TABLE socios ADD COLUMN plano_id INT NULL",
            "ALTER TABLE socios ADD COLUMN data_adesao_plano DATE NULL",
            "ALTER TABLE socios ADD COLUMN data_vencimento_plano DATE NULL",
            
            # Adicionar foreign key para plano_id se a tabela planos existir
            "ALTER TABLE socios ADD CONSTRAINT fk_socios_plano FOREIGN KEY (plano_id) REFERENCES planos(id) ON DELETE SET NULL"
        ]
        
        print("=== ADICIONANDO COLUNAS NA TABELA SOCIOS ===")
        
        for i, sql in enumerate(alteracoes, 1):
            try:
                print(f"[{i}/{len(alteracoes)}] Executando: {sql[:50]}...")
                db.execute_query(sql)
                print(f"[OK] Sucesso!")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"[INFO] Coluna ja existe - pulando")
                elif "Duplicate key name" in str(e):
                    print(f"[INFO] Chave estrangeira ja existe - pulando")
                elif "Foreign key constraint" in str(e):
                    print(f"[INFO] Problema com chave estrangeira - pulando")
                else:
                    print(f"[ERRO] {e}")
        
        print("\n=== VERIFICANDO ESTRUTURA FINAL ===")
        
        # Verificar estrutura final
        structure_query = "DESCRIBE socios"
        result = db.execute_query(structure_query, fetch=True)
        
        if result:
            print("Colunas na tabela socios:")
            for column in result:
                print(f"  - {column['Field']} ({column['Type']})")
        
        print("\n[SUCESSO] Tabela socios corrigida!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro geral: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("Corrigindo tabela socios...")
    print("=" * 50)
    fix_socios_table()
