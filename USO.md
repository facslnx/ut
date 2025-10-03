# 📖 Guia de Uso - UT-SOCIOS Streamlit

## 🎯 Visão Geral

O UT-SOCIOS é um sistema web moderno para gestão de associações esportivas, desenvolvido em Python com Streamlit. Ele substitui o sistema PHP original com uma interface mais moderna e funcionalidades aprimoradas.

## 🚀 Primeiros Passos

### 1. **Acessar o Sistema**
- Abra seu navegador
- Acesse: `http://localhost:8501`
- Faça login com as credenciais padrão

### 2. **Login Padrão**
- **Email:** fernando@f5desenvolve.com.br
- **Senha:** 123

## 📱 Navegação

### **Sidebar (Menu Lateral)**
- 🏠 **Dashboard** - Visão geral do sistema
- 👥 **Sócios** - Gestão de membros
- 🏛️ **Comandos** - Gestão de grupos/equipes
- 💰 **Faturas** - Gestão de mensalidades
- 👤 **Usuários** - Gestão de administradores

## 🏠 Dashboard

### **Métricas Principais**
- **Total de Sócios:** Número total de membros cadastrados
- **Faturas Pagas:** Valor total recebido
- **Faturas em Atraso:** Faturas que precisam de atenção

### **Ranking de Comandos**
- Lista dos comandos ordenados por número de sócios
- Mostra quantos sócios cada comando possui

### **Faturas em Atraso**
- Lista detalhada das faturas vencidas
- Mostra dias de atraso e valores

## 👥 Gestão de Sócios

### **Listar Sócios**
- Visualizar todos os sócios cadastrados
- Filtros por comando e status
- Busca por nome
- Ações: Editar e Excluir

### **Novo Sócio**
1. Clique em "➕ Novo Sócio"
2. Preencha os dados obrigatórios:
   - Nome Completo
   - CPF (com validação)
   - Data de Nascimento
   - Email (com validação)
   - Telefone (com validação)
   - Tamanho da Camisa
   - Comando
3. Opcional: Upload de foto
4. Clique em "💾 Salvar"

### **Editar Sócio**
1. Na lista de sócios, clique em "✏️"
2. Modifique os dados necessários
3. Clique em "💾 Salvar"

### **Excluir Sócio**
1. Na lista de sócios, clique em "🗑️"
2. Confirme a exclusão

### **Relatório de Sócios**
- Clique em "📊 Relatório"
- Visualize estatísticas por comando
- Gráficos de distribuição

## 🏛️ Gestão de Comandos

### **Listar Comandos**
- Visualizar todos os comandos
- Ver quantos sócios cada comando possui
- Ações: Editar e Excluir

### **Novo Comando**
1. Clique em "➕ Novo Comando"
2. Digite o nome do comando
3. Clique em "💾 Salvar"

### **Editar Comando**
1. Na lista de comandos, clique em "✏️"
2. Modifique o nome
3. Clique em "💾 Salvar"

### **Excluir Comando**
- Só é possível excluir comandos sem sócios
- Comandos com sócios mostram "🔒" (bloqueado)

## 💰 Gestão de Faturas

### **Listar Faturas**
- Visualizar todas as faturas
- Filtros por comando, status e período
- Ações: Editar e Excluir

### **Nova Fatura**
1. Clique em "➕ Nova Fatura"
2. Preencha os dados:
   - Sócio
   - Comando
   - Valor (padrão: R$ 150,00)
   - Data de Vencimento
   - Data de Renovação
   - Forma de Pagamento
3. Opcional: Upload de comprovante
4. Clique em "💾 Salvar"

### **Editar Fatura**
1. Na lista de faturas, clique em "✏️"
2. Modifique os dados necessários
3. Para marcar como pago:
   - Preencha a Data de Pagamento
   - Altere o Status para "Pago"
4. Clique em "💾 Salvar"

### **Status das Faturas**
- **Pendente:** Aguardando pagamento
- **Pago:** Pagamento confirmado
- **Atrasado:** Vencida e não paga

### **Relatório de Faturas**
- Clique em "📊 Relatório"
- Visualize estatísticas financeiras
- Gráficos por comando

## 👤 Gestão de Usuários

### **Listar Usuários**
- Visualizar todos os usuários do sistema
- Ver informações de cada usuário
- Ações: Editar e Excluir

### **Novo Usuário**
1. Clique em "➕ Novo Usuário"
2. Preencha os dados:
   - Nome Completo
   - Email (único)
   - Senha
   - Confirmar Senha
3. Clique em "💾 Salvar"

### **Editar Usuário**
1. Na lista de usuários, clique em "✏️"
2. Modifique os dados necessários
3. Para alterar senha, preencha os campos de senha
4. Clique em "💾 Salvar"

### **Excluir Usuário**
- Não é possível excluir seu próprio usuário
- Outros usuários podem ser excluídos

## 🔍 Filtros e Busca

### **Filtros Disponíveis**
- **Por Comando:** Filtra sócios/faturas por comando
- **Por Status:** Filtra faturas por status
- **Por Período:** Filtra faturas por período
- **Busca por Nome:** Busca sócios por nome

### **Como Usar Filtros**
1. Selecione o filtro desejado
2. A lista será atualizada automaticamente
3. Para limpar filtros, selecione "Todos"

## 📊 Relatórios

### **Relatório de Sócios**
- Estatísticas por comando
- Distribuição por tamanho de camisa
- Gráficos interativos

### **Relatório de Faturas**
- Resumo financeiro por comando
- Faturas pagas vs pendentes
- Gráficos de receita

## 🎨 Interface

### **Tema Visual**
- **Cores:** Preto (#000000) e Vermelho (#ff0000)
- **Design:** Moderno e responsivo
- **Navegação:** Sidebar intuitiva

### **Responsividade**
- Funciona em desktop, tablet e mobile
- Interface adapta automaticamente
- Componentes otimizados para touch

## ⌨️ Atalhos e Dicas

### **Navegação Rápida**
- Use a sidebar para navegar entre seções
- Botões de ação estão sempre visíveis
- Confirmações para ações destrutivas

### **Validações Automáticas**
- CPF é validado automaticamente
- Email é validado automaticamente
- Telefone é formatado automaticamente

### **Feedback Visual**
- Mensagens de sucesso (verde)
- Mensagens de erro (vermelho)
- Mensagens de aviso (amarelo)

## 🆘 Solução de Problemas

### **Erro de Conexão**
- Verifique se o MySQL está rodando
- Confirme as credenciais no arquivo .env

### **Erro de Validação**
- Verifique se todos os campos obrigatórios estão preenchidos
- Confirme se os dados estão no formato correto

### **Erro de Permissão**
- Verifique se você tem permissão para a ação
- Algumas ações são restritas (ex: excluir próprio usuário)

## 📱 Mobile

### **Uso em Dispositivos Móveis**
- Interface totalmente responsiva
- Botões otimizados para touch
- Navegação simplificada
- Formulários adaptados

---

**🎉 Aproveite o sistema UT-SOCIOS!**

Para dúvidas ou suporte, consulte a documentação técnica ou entre em contato com o administrador do sistema.
