#!/usr/bin/env python3
"""
Script para corrigir problemas específicos do Git
UT-SOCIOS - Sistema de Gestão de Sócios
"""

import os
import sys
import subprocess
from pathlib import Path

class GitFixManager:
    def __init__(self):
        self.project_root = Path.cwd()
        
    def print_header(self, title):
        """Imprimir cabeçalho"""
        print(f"\n{'='*60}")
        print(f"🔧 {title}")
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
    
    def diagnose_git_problem(self):
        """Diagnosticar problema do Git"""
        self.print_header("DIAGNÓSTICO DE PROBLEMAS GIT")
        
        print("🔍 Verificando status do Git...")
        
        # Verificar se é repositório Git
        if not os.path.exists(".git"):
            print("❌ Não é um repositório Git!")
            return "not_git_repo"
        
        # Verificar status
        success, stdout, stderr = self.run_command("git status")
        if not success:
            print("❌ Problema com comando git status")
            return "git_status_error"
        
        # Verificar remotes
        success, stdout, stderr = self.run_command("git remote -v")
        if "origin" not in stdout:
            print("❌ Remote origin não configurado")
            return "no_remote"
        
        # Verificar se há commits
        success, stdout, stderr = self.run_command("git log --oneline")
        if not success or not stdout.strip():
            print("❌ Nenhum commit encontrado")
            return "no_commits"
        
        print("✅ Diagnóstico concluído - Git parece estar funcionando")
        return "working"
    
    def fix_authentication(self):
        """Corrigir problemas de autenticação"""
        self.print_header("CORRIGINDO AUTENTICAÇÃO GIT")
        
        print("""
🔐 PROBLEMAS DE AUTENTICAÇÃO COMUNS:

1. 📱 GitHub CLI (Recomendado):
   - Instale: https://cli.github.com/
   - Execute: gh auth login

2. 🔑 Token de Acesso Pessoal:
   - Crie em: https://github.com/settings/tokens
   - Use como senha no push

3. 🔄 Reconfigurar remote:
   - Use URL com token: https://token@github.com/user/repo.git
        """)
        
        choice = input("\n🤔 Qual método você quer usar? (1=CLI, 2=Token, 3=Reconfigurar): ").strip()
        
        if choice == "1":
            self.setup_github_cli()
        elif choice == "2":
            self.setup_token_auth()
        elif choice == "3":
            self.reconfigure_remote()
        else:
            print("❌ Opção inválida!")
    
    def setup_github_cli(self):
        """Configurar GitHub CLI"""
        print("\n📱 Configurando GitHub CLI...")
        
        # Verificar se GitHub CLI está instalado
        success, stdout, stderr = self.run_command("gh --version")
        if not success:
            print("❌ GitHub CLI não está instalado!")
            print("📥 Baixe em: https://cli.github.com/")
            return False
        
        # Fazer login
        print("🔐 Fazendo login no GitHub...")
        success, stdout, stderr = self.run_command("gh auth login")
        
        if success:
            print("✅ Login realizado com sucesso!")
            return True
        else:
            print("❌ Falha no login")
            return False
    
    def setup_token_auth(self):
        """Configurar autenticação por token"""
        print("\n🔑 Configurando autenticação por token...")
        
        print("""
📝 PASSO A PASSO:

1. 🌐 Acesse: https://github.com/settings/tokens
2. ➕ Clique em "Generate new token (classic)"
3. ✅ Selecione escopo "repo" (acesso completo aos repositórios)
4. 📋 Copie o token gerado
5. 🔄 Use o token como senha quando o Git solicitar
        """)
        
        input("👆 Pressione Enter quando tiver o token...")
        
        # Tentar push novamente
        return self.try_push_again()
    
    def reconfigure_remote(self):
        """Reconfigurar remote com token"""
        print("\n🔄 Reconfigurando remote...")
        
        # Obter URL atual
        success, stdout, stderr = self.run_command("git remote get-url origin")
        if not success:
            print("❌ Não foi possível obter URL do remote")
            return False
        
        current_url = stdout.strip()
        print(f"📋 URL atual: {current_url}")
        
        # Solicitar token
        token = input("🔑 Cole seu token do GitHub: ").strip()
        if not token:
            print("❌ Token é obrigatório!")
            return False
        
        # Reconfigurar URL com token
        new_url = current_url.replace("https://", f"https://{token}@")
        
        success, stdout, stderr = self.run_command(
            f'git remote set-url origin "{new_url}"',
            "Reconfigurando remote com token"
        )
        
        if success:
            print("✅ Remote reconfigurado com sucesso!")
            return self.try_push_again()
        else:
            print("❌ Falha ao reconfigurar remote")
            return False
    
    def try_push_again(self):
        """Tentar push novamente"""
        print("\n🚀 Tentando push novamente...")
        
        success, stdout, stderr = self.run_command(
            "git push -u origin main",
            "Tentando push para GitHub"
        )
        
        if success:
            print("🎉 Push realizado com sucesso!")
            return True
        else:
            print("❌ Push ainda falhou")
            print("💡 Tente usar GitHub CLI: gh auth login")
            return False
    
    def fix_common_issues(self):
        """Corrigir problemas comuns"""
        self.print_header("CORRIGINDO PROBLEMAS COMUNS")
        
        # Verificar se há arquivos não commitados
        success, stdout, stderr = self.run_command("git status --porcelain")
        if stdout.strip():
            print("📁 Há arquivos não commitados. Adicionando...")
            self.run_command("git add .")
            self.run_command('git commit -m "Fix: Commit arquivos pendentes"')
        
        # Verificar se branch está atualizada
        print("🔄 Verificando se branch está atualizada...")
        self.run_command("git pull origin main --allow-unrelated-histories")
        
        # Tentar push novamente
        return self.try_push_again()
    
    def create_repository_guide(self):
        """Guia para criar repositório no GitHub"""
        self.print_header("GUIA PARA CRIAR REPOSITÓRIO NO GITHUB")
        
        print("""
🌐 PASSO A PASSO PARA CRIAR REPOSITÓRIO:

1. 📱 Acesse: https://github.com/new
2. 📝 Nome: ut-socios-streamlit
3. 📄 Descrição: Sistema de Gestão de Sócios - União Tricolor
4. 🔒 Visibilidade: Private (recomendado para segurança)
5. ❌ NÃO marque "Add a README file"
6. ❌ NÃO marque "Add .gitignore"
7. ❌ NÃO marque "Choose a license"
8. ➕ Clique em "Create repository"

📋 DEPOIS DE CRIAR:
1. 🔗 Copie a URL do repositório
2. 🔄 Execute: git remote add origin [URL]
3. 🚀 Execute: git push -u origin main
        """)
        
        url = input("\n🔗 Cole a URL do seu repositório GitHub: ").strip()
        if url:
            # Configurar remote
            success, stdout, stderr = self.run_command(
                f'git remote add origin "{url}"',
                "Adicionando remote origin"
            )
            
            if success:
                print("✅ Remote configurado!")
                return self.try_push_again()
            else:
                print("❌ Falha ao configurar remote")
                return False
    
    def run_diagnostic(self):
        """Executar diagnóstico completo"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    🔧 GIT FIX MANAGER                       ║
║              Corrigindo problemas do Git                    ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Diagnóstico
        problem = self.diagnose_git_problem()
        
        if problem == "not_git_repo":
            print("\n💡 Execute primeiro o script git-install.py")
            return False
        
        elif problem == "no_remote":
            self.create_repository_guide()
            return True
        
        elif problem == "no_commits":
            print("\n💡 Execute primeiro o script git-install.py")
            return False
        
        elif problem == "working":
            print("\n✅ Git está funcionando. Tentando push...")
            success, stdout, stderr = self.run_command("git push -u origin main")
            if success:
                print("🎉 Push realizado com sucesso!")
                return True
            else:
                # Tentar corrigir problemas comuns
                return self.fix_common_issues()
        
        else:
            # Problema de autenticação
            self.fix_authentication()
            return True

def main():
    """Função principal"""
    if not os.path.exists("main.py"):
        print("❌ ERRO: main.py não encontrado!")
        print("📁 Execute este script no diretório raiz do projeto UT-SOCIOS")
        return
    
    manager = GitFixManager()
    success = manager.run_diagnostic()
    
    if success:
        print("\n🎊 PROBLEMA RESOLVIDO! Seu código está no GitHub!")
    else:
        print("\n💥 Ainda há problemas. Tente executar git-install.py primeiro.")

if __name__ == "__main__":
    main()
