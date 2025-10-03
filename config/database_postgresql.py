import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import os
import urllib.parse as urlparse
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        # Verificar se está no Railway (DATABASE_URL presente)
        if 'DATABASE_URL' in os.environ:
            # Parse DATABASE_URL (Railway PostgreSQL format)
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            self.host = url.hostname
            self.database = url.path[1:]  # Remove leading slash
            self.user = url.username
            self.password = url.password
            self.port = url.port or 5432
        else:
            # Fallback para desenvolvimento local
            self.host = os.getenv('DB_HOST', 'localhost')
            self.database = os.getenv('DB_NAME', 'ut_socios')
            self.user = os.getenv('DB_USER', 'postgres')
            self.password = os.getenv('DB_PASSWORD', '')
            self.port = int(os.getenv('DB_PORT', '5432'))
        
        self.connection = None
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                connect_timeout=60
            )
            self.connection.autocommit = True
            return True
        except Exception as e:
            st.error(f"Erro ao conectar com o banco: {e}")
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        try:
            if not self.connection or self.connection.closed:
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                cursor.close()
                return True
        except Exception as e:
            print(f"Erro na query: {e}")
            if 'st' in globals():
                st.error(f"Erro na query: {e}")
            return None
    
    def execute_query_one(self, query, params=None):
        try:
            if not self.connection or self.connection.closed:
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Erro na query: {e}")
            if 'st' in globals():
                st.error(f"Erro na query: {e}")
            return None

# Instância global do banco
db = Database()
