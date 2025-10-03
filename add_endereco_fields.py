#!/usr/bin/env python3
"""
Script para adicionar campos de endereço na tabela socios
"""

from config.database import db

def add_endereco_fields():
    """Adicionar campos de endereço na tabela socios"""
    
    # Conectar ao banco
    if not db.connect():
        print("[ERRO] Erro ao conectar com o banco de dados")
        return False
    
    try:
        # Adicionar colunas de endereço
        alteracoes = [
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS endereco VARCHAR(255) NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS numero VARCHAR(20) NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS complemento VARCHAR(100) NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS bairro VARCHAR(100) NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS cidade VARCHAR(100) NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS estado CHAR(2) NULL",
            "ALTER TABLE socios ADD COLUMN IF NOT EXISTS cep VARCHAR(10) NULL"
        ]
        
        for sql in alteracoes:
            try:
                db.execute_query(sql)
                campo = sql.split()[-3]
                print(f"[OK] Coluna '{campo}' adicionada com sucesso")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    campo = sql.split()[-3]
                    print(f"[INFO] Coluna '{campo}' ja existe")
                else:
                    print(f"[ERRO] {e}")
        
        print("\n[SUCESSO] Campos de endereco configurados!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro geral: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("Adicionando campos de endereco...")
    print("=" * 50)
    add_endereco_fields()


