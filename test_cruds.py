#!/usr/bin/env python3
"""
Script para testar todos os CRUDs do sistema UT-SOCIOS
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import db
from utils.validators import validate_cpf, validate_email, validate_phone

def test_database_connection():
    """Testar conexão com banco de dados"""
    print("🔌 Testando conexão com banco de dados...")
    if db.connect():
        print("✅ Conexão com banco estabelecida com sucesso!")
        return True
    else:
        print("❌ Erro ao conectar com banco de dados!")
        return False

def test_comandos_crud():
    """Testar CRUD de Comandos"""
    print("\n🏛️ Testando CRUD de Comandos...")
    
    try:
        # CREATE
        print("  📝 Testando criação de comando...")
        create_query = "INSERT INTO comandos (nome) VALUES (%s)"
        if db.execute_query(create_query, ("Comando Teste",)):
            print("  ✅ Comando criado com sucesso!")
        else:
            print("  ❌ Erro ao criar comando!")
            return False
        
        # READ
        print("  📖 Testando leitura de comandos...")
        read_query = "SELECT * FROM comandos WHERE nome = %s"
        comando = db.execute_query_one(read_query, ("Comando Teste",))
        if comando:
            print(f"  ✅ Comando encontrado: {comando['nome']}")
            comando_id = comando['id']
        else:
            print("  ❌ Erro ao ler comando!")
            return False
        
        # UPDATE
        print("  ✏️ Testando atualização de comando...")
        update_query = "UPDATE comandos SET nome = %s WHERE id = %s"
        if db.execute_query(update_query, ("Comando Teste Atualizado", comando_id)):
            print("  ✅ Comando atualizado com sucesso!")
        else:
            print("  ❌ Erro ao atualizar comando!")
            return False
        
        # DELETE
        print("  🗑️ Testando exclusão de comando...")
        delete_query = "DELETE FROM comandos WHERE id = %s"
        if db.execute_query(delete_query, (comando_id,)):
            print("  ✅ Comando excluído com sucesso!")
        else:
            print("  ❌ Erro ao excluir comando!")
            return False
        
        print("  ✅ CRUD de Comandos funcionando perfeitamente!")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro no CRUD de Comandos: {e}")
        return False

def test_usuarios_crud():
    """Testar CRUD de Usuários"""
    print("\n👤 Testando CRUD de Usuários...")
    
    try:
        from utils.helpers import hash_password
        
        # CREATE
        print("  📝 Testando criação de usuário...")
        senha_hash = hash_password("123456")
        create_query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        if db.execute_query(create_query, ("Usuário Teste", "teste@teste.com", senha_hash)):
            print("  ✅ Usuário criado com sucesso!")
        else:
            print("  ❌ Erro ao criar usuário!")
            return False
        
        # READ
        print("  📖 Testando leitura de usuários...")
        read_query = "SELECT * FROM usuarios WHERE email = %s"
        usuario = db.execute_query_one(read_query, ("teste@teste.com",))
        if usuario:
            print(f"  ✅ Usuário encontrado: {usuario['nome']}")
            usuario_id = usuario['id']
        else:
            print("  ❌ Erro ao ler usuário!")
            return False
        
        # UPDATE
        print("  ✏️ Testando atualização de usuário...")
        update_query = "UPDATE usuarios SET nome = %s WHERE id = %s"
        if db.execute_query(update_query, ("Usuário Teste Atualizado", usuario_id)):
            print("  ✅ Usuário atualizado com sucesso!")
        else:
            print("  ❌ Erro ao atualizar usuário!")
            return False
        
        # DELETE
        print("  🗑️ Testando exclusão de usuário...")
        delete_query = "DELETE FROM usuarios WHERE id = %s"
        if db.execute_query(delete_query, (usuario_id,)):
            print("  ✅ Usuário excluído com sucesso!")
        else:
            print("  ❌ Erro ao excluir usuário!")
            return False
        
        print("  ✅ CRUD de Usuários funcionando perfeitamente!")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro no CRUD de Usuários: {e}")
        return False

def test_validators():
    """Testar validadores"""
    print("\n🔍 Testando validadores...")
    
    # Teste CPF
    print("  📝 Testando validação de CPF...")
    cpf_valido = "12345678909"
    cpf_invalido = "11111111111"
    
    if validate_cpf(cpf_valido):
        print("  ✅ CPF válido aceito corretamente!")
    else:
        print("  ❌ CPF válido rejeitado incorretamente!")
        return False
    
    if not validate_cpf(cpf_invalido):
        print("  ✅ CPF inválido rejeitado corretamente!")
    else:
        print("  ❌ CPF inválido aceito incorretamente!")
        return False
    
    # Teste Email
    print("  📧 Testando validação de Email...")
    email_valido = "teste@teste.com"
    email_invalido = "email-invalido"
    
    if validate_email(email_valido):
        print("  ✅ Email válido aceito corretamente!")
    else:
        print("  ❌ Email válido rejeitado incorretamente!")
        return False
    
    if not validate_email(email_invalido):
        print("  ✅ Email inválido rejeitado corretamente!")
    else:
        print("  ❌ Email inválido aceito incorretamente!")
        return False
    
    # Teste Telefone
    print("  📱 Testando validação de Telefone...")
    telefone_valido = "11999999999"
    telefone_invalido = "123"
    
    if validate_phone(telefone_valido):
        print("  ✅ Telefone válido aceito corretamente!")
    else:
        print("  ❌ Telefone válido rejeitado incorretamente!")
        return False
    
    if not validate_phone(telefone_invalido):
        print("  ✅ Telefone inválido rejeitado corretamente!")
    else:
        print("  ❌ Telefone inválido aceito incorretamente!")
        return False
    
    print("  ✅ Todos os validadores funcionando perfeitamente!")
    return True

def main():
    """Executar todos os testes"""
    print("🧪 INICIANDO TESTES DO SISTEMA UT-SOCIOS")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    # Teste 1: Conexão com banco
    if test_database_connection():
        tests_passed += 1
    
    # Teste 2: CRUD Comandos
    if test_comandos_crud():
        tests_passed += 1
    
    # Teste 3: CRUD Usuários
    if test_usuarios_crud():
        tests_passed += 1
    
    # Teste 4: Validadores
    if test_validators():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO DOS TESTES: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema funcionando perfeitamente!")
        return True
    else:
        print("⚠️ ALGUNS TESTES FALHARAM! Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
