#!/usr/bin/env python3
"""
Script para configurar o banco de dados UT-SOCIOS
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Criar banco de dados e tabelas"""
    
    # Configurações de conexão
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'ut_socios')
    
    try:
        # Conectar sem especificar o banco
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        cursor = connection.cursor()
        
        # Criar banco de dados
        print(f"📊 Criando banco de dados '{database}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE {database}")
        
        # Criar tabelas
        print("📋 Criando tabelas...")
        
        # Tabela usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(100) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL,
            nome VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # Tabela comandos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comandos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # Tabela socios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS socios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_completo VARCHAR(255) NOT NULL,
            foto VARCHAR(255),
            cpf VARCHAR(14) NOT NULL UNIQUE,
            data_nascimento DATE NOT NULL,
            email VARCHAR(100) NOT NULL,
            telefone VARCHAR(15) NOT NULL,
            tamanho_camisa ENUM('PP', 'P', 'M', 'G', 'GG', 'XG', 'XXG') NOT NULL,
            comando_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (comando_id) REFERENCES comandos(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # Tabela faturas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS faturas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            socio_id INT NOT NULL,
            comando_id INT NOT NULL,
            valor DECIMAL(10,2) NOT NULL DEFAULT 150.00,
            data_pagamento DATE,
            data_vencimento DATE NOT NULL,
            data_renovacao DATE NOT NULL,
            forma_pagamento ENUM('A vista', 'Parcelado no Cartão', 'Dinheiro', 'Cartão a vista', 'PIX', 'Em mãos'),
            comprovante VARCHAR(255),
            status ENUM('Pendente', 'Pago', 'Atrasado') NOT NULL DEFAULT 'Pendente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (socio_id) REFERENCES socios(id) ON DELETE CASCADE,
            FOREIGN KEY (comando_id) REFERENCES comandos(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # Inserir usuário padrão
        print("👤 Criando usuário padrão...")
        cursor.execute("""
        INSERT IGNORE INTO usuarios (email, senha, nome) VALUES 
        ('fernando@f5desenvolve.com.br', '$2y$10$6KUyGFpUaSqktIZ8fpEz/uE43iYNMokhYd8KKvKZ7WoneZkrKTGGi', 'Fernando')
        """)
        
        # Inserir comandos de exemplo
        print("🏛️ Criando comandos de exemplo...")
        cursor.execute("""
        INSERT IGNORE INTO comandos (nome) VALUES 
        ('Comando A'),
        ('Comando B'),
        ('Comando C')
        """)
        
        connection.commit()
        print("✅ Banco de dados configurado com sucesso!")
        
    except Error as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

def main():
    """Função principal"""
    print("🔧 Configurando banco de dados UT-SOCIOS...")
    print("=" * 50)
    
    if create_database():
        print("\n🎉 Configuração concluída!")
        print("💡 Agora você pode executar: python run.py")
    else:
        print("\n❌ Erro na configuração!")
        print("💡 Verifique as configurações do banco no arquivo .env")

if __name__ == "__main__":
    main()
