# 🚀 **SUPABASE + RAILWAY - GUIA COMPLETO**

Sistema UT-SOCIOS com Supabase (banco) + Railway (app)

## 🎯 **VANTAGENS DESTA COMBINAÇÃO:**

- ✅ **Supabase:** Banco PostgreSQL gratuito, confiável e rápido
- ✅ **Railway:** Deploy automático do app Streamlit
- ✅ **Gratuito:** Ambos têm planos gratuitos generosos
- ✅ **Escalável:** Fácil upgrade quando necessário
- ✅ **Confiável:** Menos problemas que MySQL no Railway

---

## 🗄️ **CONFIGURANDO SUPABASE:**

### **PASSO 1: CRIAR PROJETO NO SUPABASE**
1. Acesse: https://supabase.com
2. Faça login/cadastro
3. Clique em "New Project"
4. Nome: `ut-socios`
5. Senha do banco: escolha uma forte
6. Região: escolha a mais próxima (São Paulo se disponível)
7. Clique "Create new project"

### **PASSO 2: EXECUTAR SQL NO SUPABASE**
1. No projeto criado, vá para "SQL Editor"
2. Clique em "New Query"
3. Cole o conteúdo do arquivo `supabase_setup.sql`
4. Clique "Run" para executar

### **PASSO 3: OBTER CREDENCIAIS**
1. Vá para "Settings" → "Database"
2. Copie a "Connection string"
3. Formato: `postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres`

---

## 🚀 **CONFIGURANDO RAILWAY:**

### **PASSO 1: CONFIGURAR VARIÁVEIS**
No serviço "ut" do Railway, adicione:

```
PORT=8501
DATABASE_URL=[sua connection string do Supabase]
```

### **PASSO 2: REDEPLOY**
O Railway fará redeploy automaticamente após adicionar a variável.

---

## 📋 **CHECKLIST COMPLETO:**

### **✅ SUPABASE:**
- [ ] Projeto criado
- [ ] SQL executado (tabelas criadas)
- [ ] Dados iniciais inseridos
- [ ] Connection string copiada

### **✅ RAILWAY:**
- [ ] Variável `DATABASE_URL` configurada
- [ ] Redeploy realizado
- [ ] App funcionando

### **✅ TESTE:**
- [ ] App carrega sem erros
- [ ] Login funciona: `fernando@f5desenvolve.com.br` / `123`
- [ ] Todas as funcionalidades operacionais

---

## 🔐 **LOGIN PADRÃO:**
- **Email:** fernando@f5desenvolve.com.br
- **Senha:** 123

---

## 💰 **CUSTOS:**

### **SUPABASE GRATUITO:**
- ✅ 500MB de banco
- ✅ 2GB de bandwidth
- ✅ 50,000 requests/mês
- ✅ Suporte PostgreSQL completo

### **RAILWAY GRATUITO:**
- ✅ $5 créditos/mês
- ✅ Apps privados
- ✅ Deploy automático
- ✅ SSL automático

---

## 🆘 **SOLUÇÃO DE PROBLEMAS:**

### **Erro de Conexão:**
1. Verifique se `DATABASE_URL` está correta
2. Confirme se o SQL foi executado no Supabase
3. Verifique se o projeto Supabase está ativo

### **Erro de Tabelas:**
1. Execute novamente o SQL no Supabase
2. Verifique se todas as tabelas foram criadas

### **Erro de Deploy:**
1. Verifique se `psycopg2-binary` está no requirements.txt
2. Force redeploy no Railway

---

## 🎊 **RESULTADO FINAL:**

Após configurar tudo:
- ✅ App hospedado no Railway
- ✅ Banco PostgreSQL no Supabase
- ✅ Sistema completo funcionando
- ✅ Gratuito e escalável

**🌐 Sua app estará online e funcionando perfeitamente!**
