#!/usr/bin/env python3
"""
Script para configurar banco de dados no Railway
UT-SOCIOS - Sistema de Gestão de Sócios
"""

import os
import sys
import mysql.connector
from mysql.connector import Error

class RailwayDatabaseSetup:
    def __init__(self):
        self.connection = None
        
    def print_header(self, title):
        """Imprimir cabeçalho"""
        print(f"\n{'='*60}")
        print(f"🗄️ {title}")
        print(f"{'='*60}")
        
    def get_database_config(self):
        """Obter configuração do banco"""
        self.print_header("CONFIGURAÇÃO DO BANCO DE DADOS")
        
        print("📝 Por favor, forneça as informações do banco MySQL do Railway:")
        print("💡 Você pode encontrar essas informações na dashboard do Railway")
        print("   Clique no serviço MySQL → Aba 'Connect'")
        
        host = input("🏠 Host: ").strip()
        database = input("📊 Nome do banco: ").strip()
        user = input("👤 Usuário: ").strip()
        password = input("🔑 Senha: ").strip()
        port = input("🔌 Porta (padrão 3306): ").strip() or "3306"
        
        return {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': int(port)
        }
    
    def test_connection(self, config):
        """Testar conexão com banco"""
        self.print_header("TESTANDO CONEXÃO")
        
        try:
            self.connection = mysql.connector.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
                port=config['port'],
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                print("✅ Conexão com banco estabelecida com sucesso!")
                return True
            else:
                print("❌ Falha na conexão com banco")
                return False
                
        except Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def create_tables(self):
        """Criar tabelas do sistema"""
        self.print_header("CRIANDO TABELAS DO SISTEMA")
        
        cursor = self.connection.cursor()
        
        # Tabela usuarios
        usuarios_sql = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Tabela comandos
        comandos_sql = """
        CREATE TABLE IF NOT EXISTS comandos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Tabela planos
        planos_sql = """
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
        """
        
        # Tabela socios
        socios_sql = """
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
        """
        
        # Tabela faturas
        faturas_sql = """
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
        """
        
        tables = [
            ("usuarios", usuarios_sql),
            ("comandos", comandos_sql),
            ("planos", planos_sql),
            ("socios", socios_sql),
            ("faturas", faturas_sql)
        ]
        
        for table_name, sql in tables:
            try:
                cursor.execute(sql)
                print(f"✅ Tabela '{table_name}' criada com sucesso!")
            except Error as e:
                print(f"❌ Erro ao criar tabela '{table_name}': {e}")
        
        cursor.close()
        print("✅ Todas as tabelas foram criadas!")
    
    def insert_initial_data(self):
        """Inserir dados iniciais"""
        self.print_header("INSERINDO DADOS INICIAIS")
        
        cursor = self.connection.cursor()
        
        # Inserir usuário admin
        admin_password = "123"  # Senha padrão
        import bcrypt
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin_sql = """
        INSERT IGNORE INTO usuarios (nome, email, senha) 
        VALUES (%s, %s, %s)
        """
        
        try:
            cursor.execute(admin_sql, ("Administrador", "fernando@f5desenvolve.com.br", hashed_password))
            print("✅ Usuário administrador criado!")
            print("   📧 Email: fernando@f5desenvolve.com.br")
            print("   🔑 Senha: 123")
        except Error as e:
            print(f"❌ Erro ao criar usuário admin: {e}")
        
        # Inserir planos padrão
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
        
        # Inserir comando padrão
        comando_sql = """
        INSERT IGNORE INTO comandos (nome) 
        VALUES (%s)
        """
        
        try:
            cursor.execute(comando_sql, ("Comando Principal",))
            print("✅ Comando padrão criado!")
        except Error as e:
            print(f"❌ Erro ao criar comando: {e}")
        
        self.connection.commit()
        cursor.close()
        print("✅ Dados iniciais inseridos com sucesso!")
    
    def generate_env_file(self, config):
        """Gerar arquivo .env para desenvolvimento local"""
        self.print_header("GERANDO ARQUIVO .env")
        
        env_content = f"""# Configuração do banco de dados Railway
DB_HOST={config['host']}
DB_NAME={config['database']}
DB_USER={config['user']}
DB_PASSWORD={config['password']}
DB_PORT={config['port']}

# Configuração local
# DB_HOST=localhost
# DB_NAME=ut_socios
# DB_USER=root
# DB_PASSWORD=
# DB_PORT=3306
"""
        
        try:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            print("✅ Arquivo .env criado com sucesso!")
            print("📝 Use este arquivo para desenvolvimento local")
        except Exception as e:
            print(f"❌ Erro ao criar arquivo .env: {e}")
    
    def show_railway_variables(self, config):
        """Mostrar variáveis para configurar no Railway"""
        self.print_header("VARIÁVEIS PARA CONFIGURAR NO RAILWAY")
        
        print("""
🔧 CONFIGURE ESTAS VARIÁVEIS NO RAILWAY:

1. 📱 Acesse sua app no Railway
2. ⚙️ Clique em "Variables"
3. ➕ Adicione as seguintes variáveis:

PORT=8501
DB_HOST={host}
DB_NAME={database}
DB_USER={user}
DB_PASSWORD={password}
DB_PORT={port}

🌐 SUA APP ESTARÁ DISPONÍVEL EM:
https://seu-projeto-production.up.railway.app

✅ LOGIN PADRÃO:
📧 Email: fernando@f5desenvolve.com.br
🔑 Senha: 123
        """.format(**config))
    
    def run_setup(self):
        """Executar configuração completa"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    🗄️ RAILWAY DATABASE SETUP               ║
║              Configuração do banco de dados                 ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Obter configuração
        config = self.get_database_config()
        
        # Testar conexão
        if not self.test_connection(config):
            print("❌ Não foi possível conectar ao banco!")
            return False
        
        try:
            # Criar tabelas
            self.create_tables()
            
            # Inserir dados iniciais
            self.insert_initial_data()
            
            # Gerar arquivo .env
            self.generate_env_file(config)
            
            # Mostrar variáveis para Railway
            self.show_railway_variables(config)
            
            print("\n🎊 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante configuração: {e}")
            return False
        
        finally:
            if self.connection and self.connection.is_connected():
                self.connection.close()

def main():
    """Função principal"""
    setup = RailwayDatabaseSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🎉 Banco de dados configurado! Sua app está pronta!")
    else:
        print("\n💥 Falha na configuração. Verifique as informações do banco.")

if __name__ == "__main__":
    main()
