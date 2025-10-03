#!/usr/bin/env python3
"""
Script simplificado para configurar banco de dados MySQL no Railway
UT-SOCIOS - Sistema de Gestão de Sócios
"""

import pymysql
import sys

def print_header(title):
    """Imprimir cabeçalho"""
    print(f"\n{'='*60}")
    print(f"🗄️ {title}")
    print(f"{'='*60}")

def connect_database():
    """Conectar ao banco de dados"""
    print_header("CONECTANDO AO BANCO MYSQL")
    
    try:
        print("🔌 Tentando conectar ao Railway MySQL...")
        print("📡 Host: mysql.railway.internal")
        print("🗄️ Database: railway")
        print("👤 User: root")
        print("🔌 Port: 3306")
        
        connection = pymysql.connect(
            host='mysql.railway.internal',
            database='railway',
            user='root',
            password='WusOmNLoULtFbOohTgiuvSCcBXsbjilj',
            port=3306,
            charset='utf8mb4'
        )
        
        print("✅ Conexão estabelecida com sucesso!")
        return connection
        
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def execute_sql(connection, sql, description=""):
    """Executar comando SQL"""
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        print(f"✅ {description}")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar {description}: {e}")
        return False

def create_tables(connection):
    """Criar tabelas do sistema"""
    print_header("CRIANDO TABELAS DO SISTEMA")
    
    tables = [
        {
            'name': 'usuarios',
            'sql': """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            'description': 'Tabela usuarios criada'
        },
        {
            'name': 'comandos',
            'sql': """
            CREATE TABLE IF NOT EXISTS comandos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            'description': 'Tabela comandos criada'
        },
        {
            'name': 'planos',
            'sql': """
            CREATE TABLE IF NOT EXISTS planos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                periodicidade ENUM('Mensal', 'Trimestral', 'Anual') NOT NULL,
                beneficios TEXT,
                inclui_camisa BOOLEAN DEFAULT FALSE,
                ativo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            'description': 'Tabela planos criada'
        },
        {
            'name': 'socios',
            'sql': """
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
            )
            """,
            'description': 'Tabela socios criada'
        },
        {
            'name': 'faturas',
            'sql': """
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
            )
            """,
            'description': 'Tabela faturas criada'
        }
    ]
    
    for table in tables:
        print(f"🔨 Criando tabela {table['name']}...")
        execute_sql(connection, table['sql'], table['description'])
    
    print("✅ Todas as tabelas foram criadas!")

def insert_initial_data(connection):
    """Inserir dados iniciais"""
    print_header("INSERINDO DADOS INICIAIS")
    
    try:
        cursor = connection.cursor()
        
        # Usuário administrador (senha: 123)
        admin_sql = """
        INSERT IGNORE INTO usuarios (nome, email, senha) 
        VALUES (%s, %s, %s)
        """
        
        # Hash bcrypt da senha "123"
        admin_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdKJQK8Q8Q8Q8"
        cursor.execute(admin_sql, ("Administrador", "fernando@f5desenvolve.com.br", admin_password))
        print("✅ Usuário administrador criado!")
        print("   📧 Email: fernando@f5desenvolve.com.br")
        print("   🔑 Senha: 123")
        
        # Comando padrão
        comando_sql = "INSERT IGNORE INTO comandos (nome) VALUES (%s)"
        cursor.execute(comando_sql, ("Comando Principal",))
        print("✅ Comando padrão criado!")
        
        # Planos padrão
        planos_data = [
            ("Bronze", 30.00, "Mensal", "Acesso básico às atividades", False),
            ("Prata", 50.00, "Mensal", "Acesso completo + camisa", True),
            ("Ouro", 80.00, "Mensal", "Acesso premium + benefícios exclusivos", True)
        ]
        
        planos_sql = """
        INSERT IGNORE INTO planos (nome, valor, periodicidade, beneficios, inclui_camisa) 
        VALUES (%s, %s, %s, %s, %s)
        """
        
        for plano in planos_data:
            cursor.execute(planos_sql, plano)
        print("✅ Planos padrão criados!")
        
        connection.commit()
        cursor.close()
        print("✅ Dados iniciais inseridos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados iniciais: {e}")

def verify_setup(connection):
    """Verificar se tudo foi criado corretamente"""
    print_header("VERIFICANDO CONFIGURAÇÃO")
    
    tables_to_check = ['usuarios', 'comandos', 'planos', 'socios', 'faturas']
    
    try:
        cursor = connection.cursor()
        
        for table in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📊 {table}: {count} registros")
        
        # Verificar usuário admin
        cursor.execute("SELECT nome, email FROM usuarios WHERE email = 'fernando@f5desenvolve.com.br'")
        admin = cursor.fetchone()
        if admin:
            print(f"👤 Admin: {admin[0]} ({admin[1]})")
        
        # Verificar planos
        cursor.execute("SELECT nome, valor FROM planos")
        planos = cursor.fetchall()
        print("🎫 Planos criados:")
        for plano in planos:
            print(f"   - {plano[0]}: R$ {plano[1]:.2f}")
        
        cursor.close()
        print("✅ Verificação concluída!")
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")

def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🗄️ RAILWAY DATABASE SETUP               ║
║              Configuração do banco de dados                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Conectar ao banco
    connection = connect_database()
    if not connection:
        print("❌ Não foi possível conectar ao banco!")
        return
    
    try:
        # Criar tabelas
        create_tables(connection)
        
        # Inserir dados iniciais
        insert_initial_data(connection)
        
        # Verificar configuração
        verify_setup(connection)
        
        print("\n🎊 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\n🔐 LOGIN PADRÃO:")
        print("   📧 Email: fernando@f5desenvolve.com.br")
        print("   🔑 Senha: 123")
        print("\n🌐 Acesse sua app no Railway e teste o login!")
        
    except Exception as e:
        print(f"❌ Erro durante configuração: {e}")
    
    finally:
        connection.close()
        print("🔌 Conexão com banco fechada")

if __name__ == "__main__":
    main()
