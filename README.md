# ⚽ UT-SOCIOS - Sistema de Gestão de Sócios

Sistema web moderno para gestão de associações esportivas, desenvolvido em Python com Streamlit.

## 🚀 Funcionalidades

- **Dashboard** com métricas em tempo real
- **Gestão de Sócios** (CRUD completo)
- **Gestão de Comandos** (grupos/equipes)
- **Sistema de Faturas** (mensalidades e pagamentos)
- **Gestão de Usuários** (administradores)
- **Relatórios** e gráficos interativos
- **Interface responsiva** e moderna

## 🛠️ Tecnologias

- **Python 3.8+**
- **Streamlit** (framework web)
- **MySQL** (banco de dados)
- **Pandas** (análise de dados)
- **Plotly** (gráficos)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- MySQL 5.7 ou superior
- Banco de dados `ut_socios` configurado

## 🔧 Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd APP-WEB-STEAMLIT
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados:**
```bash
# Crie o arquivo .env na raiz do projeto
DB_HOST=localhost
DB_NAME=ut_socios
DB_USER=root
DB_PASSWORD=sua_senha
```

4. **Execute o sistema:**
```bash
streamlit run main.py
```

5. **Acesse no navegador:**
```
http://localhost:8501
```

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza as mesmas tabelas do sistema PHP original:

- `usuarios` - Usuários do sistema
- `comandos` - Grupos/equipes
- `socios` - Membros da associação
- `faturas` - Mensalidades e pagamentos

## 📁 Estrutura do Projeto

```
APP-WEB-STEAMLIT/
├── main.py                 # Aplicação principal
├── requirements.txt        # Dependências
├── config/
│   ├── database.py         # Conexão com banco
├── pages/
│   ├── dashboard.py        # Dashboard principal
│   ├── socios.py          # Gestão de sócios
│   ├── comandos.py        # Gestão de comandos
│   ├── faturas.py         # Gestão de faturas
│   └── usuarios.py        # Gestão de usuários
├── utils/
│   ├── helpers.py         # Funções auxiliares
│   └── validators.py      # Validações
└── assets/
    └── logo.png           # Logo da aplicação
```

## 🚀 Deploy

### Streamlit Cloud (Gratuito)
1. Faça push para GitHub
2. Conecte no [Streamlit Cloud](https://streamlit.io/cloud)
3. Configure as variáveis de ambiente
4. Deploy automático

### VPS/Servidor
1. Instale Python e MySQL
2. Configure o banco de dados
3. Execute: `streamlit run main.py --server.port 8501`

## 🔐 Login Padrão

- **Email:** fernando@f5desenvolve.com.br
- **Senha:** 123

## 📊 Funcionalidades Principais

### Dashboard
- Total de sócios cadastrados
- Faturas pagas (total e mensal)
- Faturas em atraso
- Ranking de comandos
- Gráficos interativos

### Gestão de Sócios
- Cadastro completo com validações
- Upload de fotos
- Filtros por comando
- Busca por nome
- Relatórios detalhados

### Sistema de Faturas
- Criação automática de mensalidades
- Múltiplas formas de pagamento
- Upload de comprovantes
- Controle de status (Pendente/Pago/Atrasado)
- Relatórios financeiros

## 🎨 Interface

- **Tema escuro** (preto/vermelho)
- **Design responsivo** para mobile
- **Componentes modernos** do Streamlit
- **Navegação intuitiva** com sidebar
- **Feedback visual** em todas as ações

## 🔧 Configurações

### Banco de Dados
Configure as variáveis no arquivo `.env`:
```env
DB_HOST=localhost
DB_NAME=ut_socios
DB_USER=root
DB_PASSWORD=sua_senha
```

### Streamlit
Configure no arquivo `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#ff0000"
backgroundColor = "#000000"
secondaryBackgroundColor = "#1a1a1a"
textColor = "#ffffff"
```

## 📈 Vantagens sobre o Sistema PHP

- ✅ **Interface moderna** e responsiva
- ✅ **Desenvolvimento mais rápido**
- ✅ **Deploy mais fácil**
- ✅ **Manutenção simplificada**
- ✅ **Performance superior**
- ✅ **Gráficos interativos**
- ✅ **Validações automáticas**

## 🆘 Suporte

Para dúvidas ou problemas:
1. Verifique os logs no terminal
2. Confirme a conexão com o banco
3. Verifique as dependências instaladas

## 📝 Licença

Este projeto é de uso interno da União Tricolor.

---

**Desenvolvido com ❤️ para a União Tricolor**
