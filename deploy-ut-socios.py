#!/usr/bin/env python3
"""
Script principal para deploy completo do UT-SOCIOS
Sistema de Gestão de Sócios - União Tricolor
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class UTDeployManager:
    def __init__(self):
        self.project_root = Path.cwd()
        
    def print_banner(self):
        """Imprimir banner"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 UT-SOCIOS DEPLOY                       ║
║              Sistema de Gestão de Sócios                    ║
║                    União Tricolor                           ║
╚══════════════════════════════════════════════════════════════╝

🎯 Este script irá preparar seu projeto para deploy no Railway
🔒 De forma segura e privada
⚡ Automatizando todo o processo

        """)
    
    def check_requirements(self):
        """Verificar requisitos"""
        print("🔍 VERIFICANDO REQUISITOS...")
        
        # Verificar se estamos no diretório correto
        if not os.path.exists("main.py"):
            print("❌ ERRO: main.py não encontrado!")
            print("📁 Execute este script no diretório raiz do projeto UT-SOCIOS")
            return False
        
        # Verificar se Python está instalado
        try:
            import streamlit
            print("✅ Streamlit encontrado")
        except ImportError:
            print("⚠️ Streamlit não encontrado, mas continuando...")
            print("📥 Será instalado durante o processo")
        
        print("✅ Todos os requisitos estão atendidos!")
        return True
    
    def run_script(self, script_name, description):
        """Executar script Python"""
        print(f"\n{'='*60}")
        print(f"🔧 {description}")
        print(f"{'='*60}")
        
        if not os.path.exists(script_name):
            print(f"❌ Script {script_name} não encontrado!")
            return False
        
        try:
            result = subprocess.run([sys.executable, script_name], cwd=self.project_root)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Erro ao executar {script_name}: {e}")
            return False
    
    def show_menu(self):
        """Mostrar menu principal"""
        while True:
            print(f"\n{'='*60}")
            print("🎯 MENU PRINCIPAL - UT-SOCIOS DEPLOY")
            print(f"{'='*60}")
            print("1. 🔧 Configurar Git e fazer upload para GitHub")
            print("2. 🔄 Corrigir problemas do Git")
            print("3. 🗄️ Configurar banco de dados no Railway")
            print("4. 🚀 Deploy completo (todos os passos)")
            print("5. 📋 Ver guia do Railway")
            print("6. ❌ Sair")
            print(f"{'='*60}")
            
            choice = input("🤔 Escolha uma opção (1-6): ").strip()
            
            if choice == "1":
                self.run_git_setup()
            elif choice == "2":
                self.run_git_fix()
            elif choice == "3":
                self.run_database_setup()
            elif choice == "4":
                self.run_complete_deploy()
            elif choice == "5":
                self.show_railway_guide()
            elif choice == "6":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida!")
    
    def run_git_setup(self):
        """Executar configuração do Git"""
        print("\n🔧 CONFIGURANDO GIT E GITHUB...")
        
        if self.run_script("git-install.py", "Configurando Git e fazendo upload para GitHub"):
            print("\n🎉 Git configurado com sucesso!")
            print("✅ Seu código está no GitHub!")
        else:
            print("\n❌ Falha na configuração do Git")
            print("💡 Tente a opção 2 para corrigir problemas")
    
    def run_git_fix(self):
        """Executar correção do Git"""
        print("\n🔄 CORRIGINDO PROBLEMAS DO GIT...")
        
        if self.run_script("git-fix.py", "Corrigindo problemas do Git"):
            print("\n🎉 Problemas do Git corrigidos!")
        else:
            print("\n❌ Ainda há problemas com o Git")
            print("💡 Verifique se o repositório GitHub foi criado")
    
    def run_database_setup(self):
        """Executar configuração do banco"""
        print("\n🗄️ CONFIGURANDO BANCO DE DADOS...")
        
        if self.run_script("railway-setup.py", "Configurando banco de dados no Railway"):
            print("\n🎉 Banco de dados configurado!")
            print("✅ Sua app está pronta para usar!")
        else:
            print("\n❌ Falha na configuração do banco")
            print("💡 Verifique as informações do banco MySQL no Railway")
    
    def run_complete_deploy(self):
        """Executar deploy completo"""
        print("\n🚀 INICIANDO DEPLOY COMPLETO...")
        
        steps = [
            ("git-install.py", "1. Configurando Git e GitHub"),
            ("railway-setup.py", "2. Configurando banco de dados")
        ]
        
        for script, description in steps:
            print(f"\n{description}")
            if not self.run_script(script, description):
                print(f"\n❌ Falha no passo: {description}")
                print("💡 Tente executar os passos individualmente")
                return False
            
            print(f"✅ {description} - Concluído!")
            time.sleep(2)
        
        print("\n🎊 DEPLOY COMPLETO REALIZADO COM SUCESSO!")
        self.show_final_instructions()
        return True
    
    def show_railway_guide(self):
        """Mostrar guia do Railway"""
        print(f"""
{'='*70}
🚀 GUIA COMPLETO DO RAILWAY
{'='*70}

📱 PASSO 1: ACESSAR RAILWAY
   • Acesse: https://railway.app
   • Faça login com GitHub

🏗️ PASSO 2: CRIAR PROJETO
   • Clique em "New Project"
   • Selecione "Deploy from GitHub repo"
   • Escolha seu repositório: ut-socios-streamlit
   • Clique em "Deploy Now"

🗄️ PASSO 3: ADICIONAR BANCO MYSQL
   • Na dashboard do projeto
   • Clique em "+ New"
   • Selecione "Database" → "MySQL"
   • Aguarde a criação (2-3 minutos)

⚙️ PASSO 4: CONFIGURAR VARIÁVEIS
   • Clique na aba "Variables"
   • Adicione as variáveis do banco (use o script railway-setup.py)

🌐 PASSO 5: CONFIGURAR DOMÍNIO
   • Clique na aba "Settings"
   • Clique em "Generate Domain"
   • Sua app estará em: https://seu-projeto-production.up.railway.app

✅ LOGIN PADRÃO:
   📧 Email: fernando@f5desenvolve.com.br
   🔑 Senha: 123

💰 CUSTO:
   • Gratuito para começar ($5 créditos/mês)
   • Apps privados incluídos
   • Banco MySQL incluído

🎯 RESULTADO:
   • App privado e seguro
   • Deploy automático
   • SSL automático
   • Logs em tempo real

{'='*70}
        """)
    
    def show_final_instructions(self):
        """Mostrar instruções finais"""
        print(f"""
{'='*70}
🎊 DEPLOY CONCLUÍDO COM SUCESSO!
{'='*70}

✅ O QUE FOI FEITO:
   • Código enviado para GitHub
   • Arquivos de configuração criados
   • Banco de dados configurado
   • Tabelas e dados iniciais criados

🚀 PRÓXIMOS PASSOS:
   1. 📱 Acesse: https://railway.app
   2. 🏗️ Crie novo projeto
   3. 📂 Conecte com seu repositório GitHub
   4. 🗄️ Adicione banco MySQL
   5. ⚙️ Configure variáveis de ambiente
   6. 🌐 Configure domínio

🎯 SUA APP ESTARÁ DISPONÍVEL EM:
   https://seu-projeto-production.up.railway.app

🔐 LOGIN:
   📧 Email: fernando@f5desenvolve.com.br
   🔑 Senha: 123

📞 SUPORTE:
   • Use a opção 5 para ver o guia completo
   • Verifique os logs no Railway se houver problemas
   • Todos os scripts estão disponíveis para execução individual

{'='*70}
        """)
    
    def run(self):
        """Executar aplicação principal"""
        self.print_banner()
        
        if not self.check_requirements():
            return
        
        print("🎯 Bem-vindo ao assistente de deploy do UT-SOCIOS!")
        print("💡 Este script irá te guiar através de todo o processo")
        
        self.show_menu()

def main():
    """Função principal"""
    try:
        deploy_manager = UTDeployManager()
        deploy_manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Deploy cancelado pelo usuário!")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        print("💡 Tente executar os scripts individualmente")

if __name__ == "__main__":
    main()
