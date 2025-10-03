#!/usr/bin/env python3
"""
Script automático para configuração Git e deploy no Railway
UT-SOCIOS - Sistema de Gestão de Sócios
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class GitDeployManager:
    def __init__(self):
        self.project_root = Path.cwd()
        self.git_initialized = False
        self.remote_added = False
        
    def print_step(self, step, description):
        """Imprimir passo atual"""
        print(f"\n{'='*60}")
        print(f"🔧 PASSO {step}: {description}")
        print(f"{'='*60}")
        
    def run_command(self, command, description=""):
        """Executar comando e capturar resultado"""
        print(f"⚡ Executando: {command}")
        if description:
            print(f"📝 {description}")
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print(f"✅ Sucesso!")
                if result.stdout.strip():
                    print(f"📤 Saída: {result.stdout.strip()}")
                return True, result.stdout, result.stderr
            else:
                print(f"❌ Erro!")
                if result.stderr.strip():
                    print(f"🚨 Erro: {result.stderr.strip()}")
                return False, result.stdout, result.stderr
                
        except Exception as e:
            print(f"💥 Exceção: {e}")
            return False, "", str(e)
    
    def check_git_installed(self):
        """Verificar se Git está instalado"""
        print("\n🔍 Verificando se Git está instalado...")
        success, stdout, stderr = self.run_command("git --version")
        
        if not success:
            print("❌ Git não está instalado!")
            print("📥 Baixe e instale o Git em: https://git-scm.com/downloads")
            return False
        
        print(f"✅ Git encontrado: {stdout.strip()}")
        return True
    
    def initialize_git(self):
        """Inicializar repositório Git"""
        self.print_step(1, "INICIALIZANDO REPOSITÓRIO GIT")
        
        # Verificar se já é um repositório Git
        if os.path.exists(".git"):
            print("✅ Repositório Git já inicializado")
            self.git_initialized = True
            return True
        
        # Inicializar Git
        success, stdout, stderr = self.run_command("git init", "Inicializando repositório Git")
        
        if success:
            self.git_initialized = True
            print("✅ Repositório Git inicializado com sucesso!")
            return True
        else:
            print("❌ Falha ao inicializar Git")
            return False
    
    def create_gitignore(self):
        """Criar arquivo .gitignore"""
        self.print_step(2, "CRIANDO ARQUIVO .gitignore")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.production

# Streamlit
.streamlit/secrets.toml

# Database
*.db
*.sqlite3

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads (opcional)
uploads/

# Railway
.railway/
"""
        
        try:
            with open(".gitignore", "w", encoding="utf-8") as f:
                f.write(gitignore_content)
            print("✅ Arquivo .gitignore criado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar .gitignore: {e}")
            return False
    
    def create_railway_toml(self):
        """Criar arquivo railway.toml"""
        self.print_step(3, "CRIANDO ARQUIVO railway.toml")
        
        railway_content = """[build]
builder = "NIXPACKS"

[deploy]
startCommand = "streamlit run main.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
"""
        
        try:
            with open("railway.toml", "w", encoding="utf-8") as f:
                f.write(railway_content)
            print("✅ Arquivo railway.toml criado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar railway.toml: {e}")
            return False
    
    def update_requirements_txt(self):
        """Atualizar requirements.txt"""
        self.print_step(4, "ATUALIZANDO requirements.txt")
        
        try:
            # Ler arquivo atual
            with open("requirements.txt", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Adicionar pymysql se não estiver presente
            if "pymysql" not in content:
                content += "\npymysql==1.1.0\n"
                
                with open("requirements.txt", "w", encoding="utf-8") as f:
                    f.write(content)
                print("✅ requirements.txt atualizado com pymysql!")
            else:
                print("✅ pymysql já está presente no requirements.txt")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar requirements.txt: {e}")
            return False
    
    def configure_git_user(self):
        """Configurar usuário Git"""
        self.print_step(5, "CONFIGURANDO USUÁRIO GIT")
        
        # Solicitar informações do usuário
        print("\n📝 Por favor, forneça suas informações do Git:")
        name = input("👤 Nome completo: ").strip()
        email = input("📧 Email: ").strip()
        
        if not name or not email:
            print("❌ Nome e email são obrigatórios!")
            return False
        
        # Configurar nome
        success1, _, _ = self.run_command(f'git config user.name "{name}"')
        
        # Configurar email
        success2, _, _ = self.run_command(f'git config user.email "{email}"')
        
        if success1 and success2:
            print("✅ Usuário Git configurado com sucesso!")
            return True
        else:
            print("❌ Falha ao configurar usuário Git")
            return False
    
    def add_files_to_git(self):
        """Adicionar arquivos ao Git"""
        self.print_step(6, "ADICIONANDO ARQUIVOS AO GIT")
        
        # Adicionar todos os arquivos
        success, stdout, stderr = self.run_command(
            "git add .", 
            "Adicionando todos os arquivos ao staging area"
        )
        
        if success:
            print("✅ Arquivos adicionados com sucesso!")
            
            # Verificar status
            self.run_command("git status", "Verificando status dos arquivos")
            return True
        else:
            print("❌ Falha ao adicionar arquivos")
            return False
    
    def make_initial_commit(self):
        """Fazer commit inicial"""
        self.print_step(7, "FAZENDO COMMIT INICIAL")
        
        success, stdout, stderr = self.run_command(
            'git commit -m "Initial commit - UT-SOCIOS Streamlit App"',
            "Criando commit inicial"
        )
        
        if success:
            print("✅ Commit inicial criado com sucesso!")
            return True
        else:
            print("❌ Falha ao criar commit")
            return False
    
    def rename_branch_to_main(self):
        """Renomear branch para main"""
        self.print_step(8, "RENOMEANDO BRANCH PARA MAIN")
        
        success, stdout, stderr = self.run_command(
            "git branch -M main",
            "Renomeando branch atual para 'main'"
        )
        
        if success:
            print("✅ Branch renomeada para 'main'!")
            return True
        else:
            print("❌ Falha ao renomear branch")
            return False
    
    def get_github_repo_url(self):
        """Obter URL do repositório GitHub"""
        self.print_step(9, "CONFIGURANDO REPOSITÓRIO GITHUB")
        
        print("\n📝 Por favor, forneça a URL do seu repositório GitHub:")
        print("💡 Exemplo: https://github.com/seu-usuario/ut-socios-streamlit.git")
        
        repo_url = input("🔗 URL do repositório: ").strip()
        
        if not repo_url:
            print("❌ URL do repositório é obrigatória!")
            return None
        
        if not repo_url.startswith("https://github.com/"):
            print("❌ URL deve começar com 'https://github.com/'")
            return None
        
        if not repo_url.endswith(".git"):
            repo_url += ".git"
        
        return repo_url
    
    def add_remote_origin(self, repo_url):
        """Adicionar remote origin"""
        self.print_step(10, "ADICIONANDO REMOTE ORIGIN")
        
        # Verificar se remote já existe
        success, stdout, stderr = self.run_command("git remote -v")
        if "origin" in stdout:
            print("✅ Remote 'origin' já existe!")
            self.remote_added = True
            return True
        
        # Adicionar remote
        success, stdout, stderr = self.run_command(
            f'git remote add origin "{repo_url}"',
            f"Adicionando remote origin: {repo_url}"
        )
        
        if success:
            self.remote_added = True
            print("✅ Remote origin adicionado com sucesso!")
            return True
        else:
            print("❌ Falha ao adicionar remote origin")
            return False
    
    def push_to_github(self):
        """Fazer push para GitHub"""
        self.print_step(11, "FAZENDO PUSH PARA GITHUB")
        
        print("⚠️  IMPORTANTE: Certifique-se de que o repositório GitHub já foi criado!")
        print("📋 Se ainda não criou, acesse: https://github.com/new")
        input("👆 Pressione Enter quando o repositório estiver criado...")
        
        success, stdout, stderr = self.run_command(
            "git push -u origin main",
            "Fazendo push inicial para GitHub"
        )
        
        if success:
            print("🎉 Push realizado com sucesso!")
            print("✅ Seu código está agora no GitHub!")
            return True
        else:
            print("❌ Falha no push para GitHub")
            print("\n🔧 Possíveis soluções:")
            print("1. Verifique se o repositório existe no GitHub")
            print("2. Verifique se você tem permissões de escrita")
            print("3. Tente autenticar com GitHub CLI ou token")
            return False
    
    def show_next_steps(self):
        """Mostrar próximos passos"""
        self.print_step(12, "PRÓXIMOS PASSOS - DEPLOY NO RAILWAY")
        
        print("""
🚀 AGORA VOCÊ PODE FAZER O DEPLOY NO RAILWAY:

1. 📱 Acesse: https://railway.app
2. 🔐 Faça login com GitHub
3. ➕ Clique em "New Project"
4. 📂 Selecione "Deploy from GitHub repo"
5. 🎯 Escolha seu repositório: ut-socios-streamlit
6. 🚀 Clique em "Deploy Now"

📋 DEPOIS DO DEPLOY:
1. 🗄️ Adicione banco MySQL no Railway
2. ⚙️ Configure as variáveis de ambiente
3. 🌐 Configure o domínio personalizado
4. ✅ Teste a aplicação

💡 DICAS:
- O Railway irá detectar automaticamente que é um app Streamlit
- Use as variáveis de ambiente para configurar o banco
- Os logs estarão disponíveis na dashboard do Railway

🎊 PARABÉNS! Seu app UT-SOCIOS está pronto para deploy!
        """)
    
    def run_full_process(self):
        """Executar processo completo"""
        print("🚀 INICIANDO CONFIGURAÇÃO AUTOMÁTICA DO GIT E DEPLOY")
        print("=" * 70)
        
        # Verificar Git
        if not self.check_git_installed():
            return False
        
        # Processo de configuração
        steps = [
            ("Inicializando Git", self.initialize_git),
            ("Criando .gitignore", self.create_gitignore),
            ("Criando railway.toml", self.create_railway_toml),
            ("Atualizando requirements.txt", self.update_requirements_txt),
            ("Configurando usuário Git", self.configure_git_user),
            ("Adicionando arquivos", self.add_files_to_git),
            ("Fazendo commit", self.make_initial_commit),
            ("Renomeando branch", self.rename_branch_to_main),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ FALHA NO PASSO: {step_name}")
                print("🛑 Processo interrompido!")
                return False
        
        # Configurar repositório
        repo_url = self.get_github_repo_url()
        if not repo_url:
            return False
        
        if not self.add_remote_origin(repo_url):
            return False
        
        # Push para GitHub
        if not self.push_to_github():
            return False
        
        # Mostrar próximos passos
        self.show_next_steps()
        
        print("\n🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        return True

def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 UT-SOCIOS DEPLOY                       ║
║              Configuração Automática Git + Railway          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("main.py"):
        print("❌ ERRO: main.py não encontrado!")
        print("📁 Execute este script no diretório raiz do projeto UT-SOCIOS")
        return
    
    # Executar processo
    manager = GitDeployManager()
    success = manager.run_full_process()
    
    if success:
        print("\n🎊 SUCESSO! Seu projeto está pronto para deploy no Railway!")
    else:
        print("\n💥 FALHA! Verifique os erros acima e tente novamente.")

if __name__ == "__main__":
    main()
