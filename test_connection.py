#!/usr/bin/env python3
"""
Script para testar a conexão com o banco de dados
"""

import sys
import os
from dotenv import load_dotenv

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import Database

def test_connection():
    """Testar conexão com o banco de dados"""
    print("🔍 Testando conexão com o banco de dados...")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Mostrar configurações
    print(f"📊 Host: {os.getenv('DB_HOST', 'localhost')}")
    print(f"📊 Database: {os.getenv('DB_NAME', 'ut_socios')}")
    print(f"📊 User: {os.getenv('DB_USER', 'root')}")
    print(f"📊 Password: {'*' * len(os.getenv('DB_PASSWORD', ''))}")
    print()
    
    try:
        # Testar conexão
        db = Database()
        
        if db.connect():
            print("✅ Conexão com banco de dados: OK")
            
            # Testar query simples
            result = db.execute_query_one("SELECT 1 as test")
            if result:
                print("✅ Query de teste: OK")
            
            # Verificar tabelas
            tables_query = "SHOW TABLES"
            tables = db.execute_query(tables_query, fetch=True)
            
            if tables:
                print("✅ Tabelas encontradas:")
                for table in tables:
                    table_name = list(table.values())[0]
                    print(f"   - {table_name}")
            else:
                print("⚠️  Nenhuma tabela encontrada")
                print("💡 Execute: python setup_database.py")
            
            # Verificar usuários
            users_query = "SELECT COUNT(*) as total FROM usuarios"
            users_result = db.execute_query_one(users_query)
            if users_result:
                print(f"✅ Usuários cadastrados: {users_result['total']}")
            
            db.disconnect()
            print("\n🎉 Teste concluído com sucesso!")
            return True
            
        else:
            print("❌ Erro na conexão com banco de dados")
            print("💡 Verifique:")
            print("   - MySQL está rodando?")
            print("   - Credenciais corretas no .env?")
            print("   - Banco 'ut_socios' existe?")
            return False
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("💡 Verifique as dependências: pip install -r requirements.txt")
        return False

def main():
    """Função principal"""
    print("🧪 Teste de Conexão - UT-SOCIOS")
    print("=" * 50)
    
    if test_connection():
        print("\n✅ Sistema pronto para uso!")
        print("💡 Execute: python run.py")
    else:
        print("\n❌ Problemas encontrados!")
        print("💡 Consulte o arquivo INSTALACAO.md")

if __name__ == "__main__":
    main()
