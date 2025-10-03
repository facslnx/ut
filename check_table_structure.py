#!/usr/bin/env python3
"""
Script para verificar a estrutura da tabela socios
"""

from config.database import db

def check_table_structure():
    """Verificar estrutura da tabela socios"""
    
    # Conectar ao banco
    if not db.connect():
        print("[ERRO] Erro ao conectar com o banco de dados")
        return False
    
    try:
        # Verificar estrutura da tabela socios
        print("=== ESTRUTURA DA TABELA SOCIOS ===")
        structure_query = "DESCRIBE socios"
        result = db.execute_query(structure_query, fetch=True)
        
        if result:
            for column in result:
                print(f"Coluna: {column['Field']} | Tipo: {column['Type']} | Null: {column['Null']} | Key: {column['Key']}")
        else:
            print("Não foi possível obter a estrutura da tabela")
        
        print("\n=== VERIFICANDO SE PLANO_ID EXISTE ===")
        check_plano_query = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'socios' AND COLUMN_NAME = 'plano_id'
        """
        plano_result = db.execute_query(check_plano_query, fetch=True)
        
        if plano_result:
            print("[OK] Coluna 'plano_id' existe na tabela socios")
        else:
            print("[ERRO] Coluna 'plano_id' NAO existe na tabela socios")
        
        print("\n=== VERIFICANDO SE CAMPOS DE ENDERECO EXISTEM ===")
        endereco_fields = ['cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
        for field in endereco_fields:
            check_query = f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'socios' AND COLUMN_NAME = '{field}'
            """
            field_result = db.execute_query(check_query, fetch=True)
            if field_result:
                print(f"[OK] Coluna '{field}' existe")
            else:
                print(f"[ERRO] Coluna '{field}' NAO existe")
        
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro geral: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("Verificando estrutura da tabela socios...")
    print("=" * 50)
    check_table_structure()
