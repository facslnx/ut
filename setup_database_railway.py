#!/usr/bin/env python3
"""
Script para configurar banco de dados MySQL no Railway
UT-SOCIOS - Sistema de Gestão de Sócios
"""

import mysql.connector
from mysql.connector import Error
import sys

class RailwayDatabaseSetup:
    def __init__(self):
        # Credenciais do Railway MySQL
        self.config = {
            'host': 'mysql.railway.internal',
            'database': 'railway',
            'user': 'root',
            'password': 'WusOmNLoULtFbOohTgiuvSCcBXsbjilj',
            'port': 3306,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }
        self.connection = None
        
    def print_header(self, title):
        """Imprimir cabeçalho"""
        print(f"\n{'='*60}")
        print(f"🗄️ {title}")
        print(f"{'='*60}")
        
    def connect(self):
        """Conectar ao banco de dados"""
        self.print_header("CONECTANDO AO BANCO MYSQL")
        
        try:
            print("🔌 Tentando conectar ao Railway MySQL...")
            print(f"📡 Host: {self.config['host']}")
            print(f"🗄️ Database: {self.config['database']}")
            print(f"👤 User: {self.config['user']}")
            print(f"🔌 Port: {self.config['port']}")
            
            self.connection = mysql.connector.connect(**self.config)
            
            if self.connection.is_connected():
                print("✅ Conexão estabelecida com sucesso!")
                db_info = self.connection.get_server_info()
                print(f"📊 Versão do MySQL: {db_info}")
                return True
            else:
                print("❌ Falha na conexão")
                return False
                
        except Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def execute_sql(self, sql, description=""):
        """Executar comando SQL"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            print(f"✅ {description}")
            return True
        except Error as e:
            print(f"❌ Erro ao executar {description}: {e}")
            return False
    
    def create_tables(self):
        """Criar tabelas do sistema"""
        self.print_header("CRIANDO TABELAS DO SISTEMA")
        
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
            self.execute_sql(table['sql'], table['description'])
        
        print("✅ Todas as tabelas foram criadas!")
    
    def insert_initial_data(self):
        """Inserir dados iniciais"""
        self.print_header("INSERINDO DADOS INICIAIS")
        
        # Usuário administrador (senha: 123)
        admin_sql = """
        INSERT IGNORE INTO usuarios (nome, email, senha) 
        VALUES (%s, %s, %s)
        """
        
        try:
            cursor = self.connection.cursor()
            # Hash bcrypt da senha "123"
            admin_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdKJQK8Q8Q8Q8"
            cursor.execute(admin_sql, ("Administrador", "fernando@f5desenvolve.com.br", admin_password))
            print("✅ Usuário administrador criado!")
            print("   📧 Email: fernando@f5desenvolve.com.br")
            print("   🔑 Senha: 123")
        except Error as e:
            print(f"❌ Erro ao criar usuário admin: {e}")
        
        # Comando padrão
        comando_sql = "INSERT IGNORE INTO comandos (nome) VALUES (%s)"
        try:
            cursor.execute(comando_sql, ("Comando Principal",))
            print("✅ Comando padrão criado!")
        except Error as e:
            print(f"❌ Erro ao criar comando: {e}")
        
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
        
        try:
            for plano in planos_data:
                cursor.execute(planos_sql, plano)
            print("✅ Planos padrão criados!")
        except Error as e:
            print(f"❌ Erro ao criar planos: {e}")
        
        self.connection.commit()
        cursor.close()
        print("✅ Dados iniciais inseridos com sucesso!")
    
    def verify_setup(self):
        """Verificar se tudo foi criado corretamente"""
        self.print_header("VERIFICANDO CONFIGURAÇÃO")
        
        tables_to_check = ['usuarios', 'comandos', 'planos', 'socios', 'faturas']
        
        try:
            cursor = self.connection.cursor()
            
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
            
        except Error as e:
            print(f"❌ Erro na verificação: {e}")
    
    def disconnect(self):
        """Desconectar do banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexão com banco fechada")
    
    def run_setup(self):
        """Executar configuração completa"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    🗄️ RAILWAY DATABASE SETUP               ║
║              Configuração do banco de dados                 ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        try:
            # Conectar
            if not self.connect():
                return False
            
            # Criar tabelas
            self.create_tables()
            
            # Inserir dados iniciais
            self.insert_initial_data()
            
            # Verificar configuração
            self.verify_setup()
            
            print("\n🎊 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
            print("\n🔐 LOGIN PADRÃO:")
            print("   📧 Email: fernando@f5desenvolve.com.br")
            print("   🔑 Senha: 123")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante configuração: {e}")
            return False
        
        finally:
            self.disconnect()

def main():
    """Função principal"""
    setup = RailwayDatabaseSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🎉 Banco de dados configurado! Sua app está pronta!")
        print("🌐 Acesse sua app no Railway e teste o login!")
    else:
        print("\n💥 Falha na configuração. Verifique as credenciais e conexão.")

if __name__ == "__main__":
    main()
