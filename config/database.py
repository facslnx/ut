import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        # Modo offline - sem conexão com banco
        self.connection = None
        self.offline_mode = True
    
    def connect(self):
        # Sempre retorna True em modo offline
        return True
    
    def disconnect(self):
        # Não faz nada em modo offline
        pass
    
    def execute_query(self, query, params=None, fetch=False):
        # Modo offline - retorna dados mock ou vazio
        if fetch:
            return []
        return True
    
    def execute_query_one(self, query, params=None):
        # Modo offline - retorna None
        return None

# Instância global do banco
db = Database()
