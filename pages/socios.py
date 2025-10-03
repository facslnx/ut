import streamlit as st
import pandas as pd
from config.database import db
from utils.helpers import format_date, show_success, show_error
from utils.validators import validate_cpf, validate_email, validate_phone, format_cpf, format_phone, validate_cep, format_cep
from utils.photo_manager import create_photo_upload_widget, save_socio_photo, show_socio_photo
import time
from datetime import datetime, date, timedelta

def format_endereco_completo(socio):
    """Formatar endereço completo para exibição"""
    partes = []
    
    if socio.get('endereco'):
        rua = socio['endereco']
        if socio.get('numero'):
            rua += f", {socio['numero']}"
        partes.append(rua)
    
    if socio.get('complemento'):
        partes.append(socio['complemento'])
    
    if socio.get('bairro'):
        partes.append(socio['bairro'])
    
    if socio.get('cidade') and socio.get('estado'):
        partes.append(f"{socio['cidade']}/{socio['estado']}")
    
    if socio.get('cep'):
        partes.append(f"CEP: {format_cep(socio['cep'])}")
    
    return " - ".join(partes) if partes else "Endereço não informado"

# Cache para comandos (evita consultas repetidas)
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_comandos():
    """Buscar comandos com cache"""
    try:
        comandos_query = "SELECT id, nome FROM comandos ORDER BY nome"
        result = db.execute_query(comandos_query, fetch=True)
        return result if result else []
    except Exception as e:
        st.error(f"Erro ao buscar comandos: {e}")
        return []

# Cache para planos
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_planos():
    """Buscar planos com cache"""
    try:
        planos_query = "SELECT id, nome, valor, periodicidade FROM planos WHERE ativo = TRUE ORDER BY valor"
        result = db.execute_query(planos_query, fetch=True)
        return result if result else []
    except Exception as e:
        st.error(f"Erro ao buscar planos: {e}")
        return []

@st.cache_data(ttl=60)  # Cache por 1 minuto
def get_socios_data():
    """Buscar dados de sócios com cache"""
    try:
        socios_query = """
        SELECT s.*, c.nome as comando_nome, p.nome as plano_nome, p.valor as plano_valor, p.periodicidade
        FROM socios s 
        LEFT JOIN comandos c ON s.comando_id = c.id
        LEFT JOIN planos p ON s.plano_id = p.id
        ORDER BY s.nome_completo
        """
        result = db.execute_query(socios_query, fetch=True)
        return result if result else []
    except Exception as e:
        st.error(f"Erro ao buscar sócios: {e}")
        return []

@st.cache_data(ttl=60)  # Cache por 1 minuto
def get_report_data():
    """Buscar dados do relatório com cache"""
    try:
        report_query = """
        SELECT 
            c.nome as comando,
            COUNT(s.id) as total_socios,
            COUNT(CASE WHEN s.tamanho_camisa = 'PP' THEN 1 END) as tamanho_pp,
            COUNT(CASE WHEN s.tamanho_camisa = 'P' THEN 1 END) as tamanho_p,
            COUNT(CASE WHEN s.tamanho_camisa = 'M' THEN 1 END) as tamanho_m,
            COUNT(CASE WHEN s.tamanho_camisa = 'G' THEN 1 END) as tamanho_g,
            COUNT(CASE WHEN s.tamanho_camisa = 'GG' THEN 1 END) as tamanho_gg,
            COUNT(CASE WHEN s.tamanho_camisa = 'XG' THEN 1 END) as tamanho_xg,
            COUNT(CASE WHEN s.tamanho_camisa = 'XXG' THEN 1 END) as tamanho_xxg
        FROM comandos c
        LEFT JOIN socios s ON c.id = s.comando_id
        GROUP BY c.id, c.nome
        ORDER BY total_socios DESC
        """
        result = db.execute_query(report_query, fetch=True)
        return result if result else []
    except Exception as e:
        st.error(f"Erro ao buscar dados do relatório: {e}")
        return []

@st.cache_data(ttl=60)  # Cache por 1 minuto
def get_planos_report_data():
    """Buscar dados de sócios por plano com cache"""
    try:
        planos_query = """
        SELECT 
            COALESCE(p.nome, 'Sem Plano') as plano_nome,
            COUNT(s.id) as total_socios,
            COALESCE(p.valor, 0) as valor_plano,
            COALESCE(p.periodicidade, 'N/A') as periodicidade
        FROM socios s
        LEFT JOIN planos p ON s.plano_id = p.id
        GROUP BY p.id, p.nome, p.valor, p.periodicidade
        ORDER BY total_socios DESC
        """
        result = db.execute_query(planos_query, fetch=True)
        return result if result else []
    except Exception as e:
        st.error(f"Erro ao buscar dados de planos: {e}")
        return []

def show():
    st.title("👥 Gestão de Sócios")
    st.markdown("---")
    
    # Inicializar session_state se não existir
    if 'socio_action' not in st.session_state:
        st.session_state['socio_action'] = 'list'
    
    # Botões de ação
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("➕ Novo Sócio", use_container_width=True, key="btn_novo_socio"):
            st.session_state['socio_action'] = 'create'
    
    with col2:
        if st.button("📊 Relatório", use_container_width=True, key="btn_relatorio"):
            st.session_state['socio_action'] = 'report'
    
    # Verificar ação e renderizar conteúdo
    action = st.session_state.get('socio_action', 'list')
    
    if action == 'create':
        show_create_form()
    elif action == 'edit':
        show_edit_form(st.session_state.get('socio_id'))
    elif action == 'report':
        show_report()
    else:
        show_socios_list()

def show_socios_list():
    """Mostrar lista de sócios"""
    
    # Filtros
    st.subheader("🔍 Filtros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Usar cache para comandos
        comandos = get_comandos()
        comando_options = {0: "Todos os comandos"}
        if comandos:
            comando_options.update({c['id']: c['nome'] for c in comandos})
        
        comando_filtro = st.selectbox(
            "Filtrar por Comando",
            options=list(comando_options.keys()),
            format_func=lambda x: comando_options[x]
        )
    
    with col2:
        status_filtro = st.selectbox(
            "Status",
            ["Todos", "Ativos", "Inativos"]
        )
    
    with col3:
        search_term = st.text_input("Buscar por nome")
    
    # Buscar sócios com cache
    with st.spinner("Carregando sócios..."):
        socios = get_socios_data()
    
    # Aplicar filtros localmente (mais rápido que SQL)
    if comando_filtro != 0:
        socios = [s for s in socios if s['comando_id'] == comando_filtro]
    
    if search_term:
        socios = [s for s in socios if search_term.lower() in s['nome_completo'].lower()]
    
    if socios:
        st.subheader("📋 Lista de Sócios")
        for socio in socios:
            with st.container():
                col_foto, col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2, 1])
                
                with col_foto:
                    # Mostrar foto do sócio
                    show_socio_photo(socio.get('foto'), width=60, height=60)
                
                with col1:
                    st.write(f"**{socio['nome_completo']}**")
                    st.write(f"📧 {socio['email']}")
                
                with col2:
                    st.write(f"🏛️ {socio['comando_nome']}")
                    st.write(f"📱 {format_phone(socio['telefone'])}")
                    if socio.get('cidade') and socio.get('estado'):
                        st.write(f"📍 {socio['cidade']}/{socio['estado']}")
                
                with col3:
                    st.write(f"📅 {format_date(socio['data_nascimento'])}")
                    st.write(f"👕 {socio['tamanho_camisa']}")
                
                with col4:
                    st.write(f"🆔 {format_cpf(socio['cpf'])}")
                    if socio['plano_nome']:
                        st.write(f"🎫 {socio['plano_nome']}")
                    else:
                        st.write("❌ Sem plano")
                
                with col5:
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️", key=f"edit_{socio['id']}"):
                            st.session_state['socio_action'] = 'edit'
                            st.session_state['socio_id'] = socio['id']
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_{socio['id']}"):
                            if delete_socio(socio['id']):
                                show_success("Sócio excluído com sucesso!")
                                # Limpar cache
                                get_socios_data.clear()
                                get_report_data.clear()
                                st.rerun()
                            else:
                                show_error("Erro ao excluir sócio!")
                
        st.markdown("---")
    else:
        st.info("Nenhum sócio encontrado com os filtros aplicados.")

def show_create_form():
    """Mostrar formulário de criação de sócio"""
    
    # Header com botão voltar
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ Voltar", use_container_width=True, key="btn_voltar_create"):
            st.session_state['socio_action'] = 'list'
            st.rerun()
    
    st.subheader("➕ Cadastro de Novo Sócio")
    st.markdown("---")
    
    # Verificar se há comandos disponíveis
    try:
        comandos = get_comandos()
        
        if not comandos:
            st.error("⚠️ Nenhum comando encontrado!")
            st.info("📋 Para cadastrar um sócio, é necessário ter pelo menos um comando cadastrado.")
            st.info("🔧 Vá para a seção 'Comandos' e cadastre um comando primeiro.")
            return
        
        # Formulário principal
        with st.form("novo_socio_form", clear_on_submit=True):
            
            # Seção 1: Dados Pessoais
            st.markdown("### 📋 Dados Pessoais")
            
            col1, col2 = st.columns(2)
        
            with col1:
                nome_completo = st.text_input(
                    "Nome Completo *",
                    placeholder="Digite o nome completo do sócio"
                )
                
                cpf = st.text_input(
                    "CPF *",
                    placeholder="000.000.000-00",
                    max_chars=14
                )
                
                data_nascimento = st.date_input(
                    "Data de Nascimento *",
                    value=None,
                    min_value=date(1900, 1, 1),
                    max_value=date.today()
                )
        
            with col2:
                email = st.text_input(
                    "E-mail *",
                    placeholder="exemplo@email.com"
                )
                
                telefone = st.text_input(
                    "Telefone/WhatsApp *",
                    placeholder="(00) 00000-0000",
                    max_chars=15
                )
                
                tamanho_camisa = st.selectbox(
                    "Tamanho da Camisa *",
                    options=["PP", "P", "M", "G", "GG", "XG", "XXG"]
                )
        
            st.markdown("---")
        
            # Seção 1.5: Foto do Sócio
            st.markdown("### 📸 Foto do Sócio")
            foto_uploaded = create_photo_upload_widget(
            "📸 Foto do Sócio (Opcional)",
            "Faça upload de uma foto do sócio (JPG, PNG, GIF, BMP - máx. 5MB)"
            )
        
            st.markdown("---")
        
            # Seção 2: Dados do Comando
            st.markdown("### 🏛️ Dados do Comando")
        
            comando_options = {c['id']: c['nome'] for c in comandos}
            comando_id = st.selectbox(
            "Comando *",
            options=list(comando_options.keys()),
            format_func=lambda x: comando_options[x]
            )
        
            st.markdown("---")
        
            # Seção 2.5: Data de Cadastro
            st.markdown("### 📅 Data de Cadastro")
        
            col_data1, col_data2 = st.columns(2)
        
            with col_data1:
                data_cadastro_personalizada = st.date_input(
                "Data de Cadastro",
                value=date.today(),
                min_value=date(2020, 1, 1),
                max_value=date.today(),
                help="Data em que o sócio foi cadastrado (padrão: hoje)"
            )
        
            with col_data2:
                st.info("📅 **Data de Cadastro**\n\nEsta data será registrada no sistema para controle e relatórios.")
        
            st.markdown("---")
        
            # Seção 3: Endereço
            st.markdown("### 📍 Endereço")
        
            col1, col2 = st.columns(2)
        
            with col1:
                cep = st.text_input(
                    "CEP",
                    placeholder="00000-000",
                    max_chars=9,
                    help="CEP do endereço"
                )
                
                endereco = st.text_input(
                    "Endereço (Rua/Avenida)",
                    placeholder="Ex: Rua das Flores",
                    help="Nome da rua ou avenida"
                )
                
                numero = st.text_input(
                    "Número",
                    placeholder="Ex: 123",
                    help="Número da residência"
                )
                
                complemento = st.text_input(
                    "Complemento",
                    placeholder="Ex: Apto 101, Bloco A",
                    help="Complemento (opcional)"
                )
        
            with col2:
                bairro = st.text_input(
                    "Bairro",
                    placeholder="Ex: Centro",
                    help="Nome do bairro"
                )
                
                cidade = st.text_input(
                    "Cidade",
                    placeholder="Ex: Joinville",
                    help="Nome da cidade"
                )
                
                # Estados brasileiros
                estados_br = [
                    "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                    "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                ]
                
                estado = st.selectbox(
                    "Estado (UF)",
                    options=estados_br,
                    help="Selecione o estado"
                )
            
            st.markdown("---")
            
            # Seção 4: Plano (Opcional)
            st.markdown("### 🎫 Plano de Sócio (Opcional)")
            
            # Buscar planos disponíveis
            planos_disponiveis = get_planos()
            plano_options = {0: "Sem plano"}
            if planos_disponiveis:
                plano_options.update({p['id']: f"{p['nome']} - R$ {p['valor']:.2f} ({p['periodicidade']})" for p in planos_disponiveis})
            
            plano_id = st.selectbox(
                "Plano",
                options=list(plano_options.keys()),
                format_func=lambda x: plano_options[x],
                help="Plano de sócio (opcional)."
            )
            
            st.markdown("---")
            
            # Seção 5: Botões de Ação
            st.markdown("### ✅ Ações")
        
            col1, col2, col3 = st.columns([1, 1, 4])
        
            with col1:
                submit_button = st.form_submit_button(
                    "💾 Salvar Sócio",
                    use_container_width=True,
                    type="primary"
                )
            
            with col2:
                cancel_button = st.form_submit_button(
                    "❌ Cancelar",
                    use_container_width=True
                )
            
            # Processamento do formulário
            if submit_button:
                # Validações básicas
                if not nome_completo.strip():
                    st.error("❌ Nome completo é obrigatório!")
                    return
                
                if not cpf.strip():
                    st.error("❌ CPF é obrigatório!")
                    return
                
                if not validate_cpf(cpf):
                    st.error("❌ CPF inválido!")
                    return
                
                if not email.strip():
                    st.error("❌ E-mail é obrigatório!")
                    return
                
                if not validate_email(email):
                    st.error("❌ E-mail inválido!")
                    return
                
                if not telefone.strip():
                    st.error("❌ Telefone é obrigatório!")
                    return
                
                if not validate_phone(telefone):
                    st.error("❌ Telefone inválido!")
                    return
                
                if not data_nascimento:
                    st.error("❌ Data de nascimento é obrigatória!")
                    return
                
                # Processar dados
                cpf_limpo = ''.join(filter(str.isdigit, cpf))
                telefone_limpo = ''.join(filter(str.isdigit, telefone))
                
                # Processar dados de endereço
                cep_limpo = ''.join(filter(str.isdigit, cep)) if cep else None
                
                # Processar foto
                foto_path = None
                if foto_uploaded:
                    with st.spinner("Salvando foto..."):
                        foto_path, error = save_socio_photo(foto_uploaded)
                        if error:
                            st.error(f"Erro ao salvar foto: {error}")
                            return
                
                # Salvar no banco
                plano_id_final = plano_id if plano_id != 0 else None
                endereco_data = {
                    'cep': cep_limpo,
                    'endereco': endereco.strip() if endereco else None,
                    'numero': numero.strip() if numero else None,
                    'complemento': complemento.strip() if complemento else None,
                    'bairro': bairro.strip() if bairro else None,
                    'cidade': cidade.strip() if cidade else None,
                    'estado': estado if estado else None
                }
                
                if create_socio(nome_completo.strip(), cpf_limpo, data_nascimento, email.strip().lower(), telefone_limpo, tamanho_camisa, comando_id, foto_path, plano_id_final, endereco_data, data_cadastro_personalizada):
                    show_success("✅ Sócio cadastrado com sucesso!")
                    # Limpar cache
                    get_socios_data.clear()
                    get_report_data.clear()
                    st.session_state['socio_action'] = 'list'
                    st.rerun()
                else:
                    show_error("❌ Erro ao cadastrar sócio!")
        
            elif cancel_button:
                st.session_state['socio_action'] = 'list'
                st.rerun()
    
    except Exception as e:
            st.error(f"❌ Erro no formulário: {e}")
            import traceback
            st.code(traceback.format_exc())

def show_edit_form(socio_id):
    """Mostrar formulário de edição completo"""
    
    # Header com botão voltar
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ Voltar", use_container_width=True, key="btn_voltar_edit"):
            st.session_state['socio_action'] = 'list'
            st.rerun()
    
    st.subheader(f"✏️ Editar Sócio (ID: {socio_id})")
    st.markdown("---")
    
    # Buscar dados do sócio
    socio_query = "SELECT * FROM socios WHERE id = %s"
    socio = db.execute_query_one(socio_query, (socio_id,))
    
    if not socio:
        st.error("Sócio não encontrado para edição.")
        if st.button("⬅️ Voltar para a lista", key="btn_voltar_edit_error"):
            st.session_state['socio_action'] = 'list'
            st.rerun()
        return
    
    # Verificar se há comandos disponíveis
    try:
        comandos = get_comandos()
        
        if not comandos:
            st.error("⚠️ Nenhum comando encontrado!")
            st.info("📋 Para editar um sócio, é necessário ter pelo menos um comando cadastrado.")
            st.info("🔧 Vá para a seção 'Comandos' e cadastre um comando primeiro.")
            return
        
        # Formulário principal
        with st.form("edit_socio_form", clear_on_submit=False):
            
            # Seção 1: Dados Pessoais
            st.markdown("### 📋 Dados Pessoais")
            
            col1, col2 = st.columns(2)
        
            with col1:
                nome_completo = st.text_input(
                    "Nome Completo *",
                    value=socio['nome_completo'],
                    placeholder="Digite o nome completo do sócio"
                )
                
                cpf = st.text_input(
                    "CPF *",
                    value=format_cpf(socio['cpf']) if socio['cpf'] else "",
                    placeholder="000.000.000-00",
                    max_chars=14
                )
                
                data_nascimento = st.date_input(
                    "Data de Nascimento *",
                    value=socio['data_nascimento'],
                    min_value=date(1920, 1, 1),
                    max_value=date.today()
                )
                
                email = st.text_input(
                    "Email *",
                    value=socio['email'],
                    placeholder="exemplo@dominio.com"
                )
        
            with col2:
                telefone = st.text_input(
                    "Telefone *",
                    value=format_phone(socio['telefone']) if socio['telefone'] else "",
                    placeholder="(00) 90000-0000",
                    max_chars=15
                )
                
            tamanho_camisa = st.selectbox(
                "Tamanho da Camisa *",
                    options=["PP", "P", "M", "G", "GG", "XG", "XXG"],
                index=["PP", "P", "M", "G", "GG", "XG", "XXG"].index(socio['tamanho_camisa'])
            )
            
            st.markdown("---")
            
            # Seção 1.5: Foto do Sócio
            st.markdown("### 📸 Foto do Sócio")
            
            # Mostrar foto atual se existir
            if socio.get('foto'):
                col_foto1, col_foto2 = st.columns([1, 2])
                with col_foto1:
                    show_socio_photo(socio['foto'], width=120, height=120)
                with col_foto2:
                    st.info("📸 Foto atual do sócio")
            
            # Campo para nova foto
            nova_foto_uploaded = create_photo_upload_widget(
                "📸 Nova Foto do Sócio (Opcional)",
                "Faça upload de uma nova foto para substituir a atual (JPG, PNG, GIF, BMP - máx. 5MB)"
            )
            
            st.markdown("---")
            
            # Seção 2: Dados do Comando
            st.markdown("### 🏛️ Dados do Comando")
            
            comando_options = {c['id']: c['nome'] for c in comandos}
            
            # Encontrar o índice do comando atual
            current_comando_index = 0
            if socio['comando_id'] in comando_options:
                current_comando_index = list(comando_options.keys()).index(socio['comando_id'])
            
            comando_id = st.selectbox(
                "Comando *",
                options=list(comando_options.keys()),
                format_func=lambda x: comando_options[x],
                index=current_comando_index
            )
            
            st.markdown("---")
            
            # Seção 3: Endereço
            st.markdown("### 📍 Endereço")
            
            col1, col2 = st.columns(2)
            
            with col1:
                cep = st.text_input(
                    "CEP",
                    value=format_cep(socio['cep']) if socio.get('cep') else "",
                    placeholder="00000-000",
                    max_chars=9,
                    help="CEP do endereço"
                )
                
                endereco = st.text_input(
                    "Endereço (Rua/Avenida)",
                    value=socio.get('endereco', ''),
                    placeholder="Ex: Rua das Flores",
                    help="Nome da rua ou avenida"
                )
                
                numero = st.text_input(
                    "Número",
                    value=socio.get('numero', ''),
                    placeholder="Ex: 123",
                    help="Número da residência"
                )
                
                complemento = st.text_input(
                    "Complemento",
                    value=socio.get('complemento', ''),
                    placeholder="Ex: Apto 101, Bloco A",
                    help="Complemento (opcional)"
                )
            
            with col2:
                bairro = st.text_input(
                    "Bairro",
                    value=socio.get('bairro', ''),
                    placeholder="Ex: Centro",
                    help="Nome do bairro"
                )
                
                cidade = st.text_input(
                    "Cidade",
                    value=socio.get('cidade', ''),
                    placeholder="Ex: Joinville",
                    help="Nome da cidade"
                )
                
                # Estados brasileiros
                estados_br = [
                    "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                    "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                ]
                
                # Encontrar índice do estado atual
                current_estado_index = 0
                if socio.get('estado') in estados_br:
                    current_estado_index = estados_br.index(socio['estado'])
                
                estado = st.selectbox(
                    "Estado (UF)",
                    options=estados_br,
                    index=current_estado_index,
                    help="Selecione o estado"
                )
            
            st.markdown("---")
            
            # Seção 4: Plano (Opcional)
            st.markdown("### 🎫 Plano de Sócio (Opcional)")
            
            # Buscar planos disponíveis
            planos_disponiveis = get_planos()
            plano_options = {0: "Sem plano"}
            if planos_disponiveis:
                plano_options.update({p['id']: f"{p['nome']} - R$ {p['valor']:.2f} ({p['periodicidade']})" for p in planos_disponiveis})
            
            # Encontrar índice do plano atual
            current_plano_index = 0
            if socio.get('plano_id') and socio['plano_id'] in plano_options:
                current_plano_index = list(plano_options.keys()).index(socio['plano_id'])
            
            plano_id = st.selectbox(
                "Plano",
                options=list(plano_options.keys()),
                format_func=lambda x: plano_options[x],
                index=current_plano_index,
                help="Plano de sócio (opcional)."
            )
            
            st.markdown("---")
            
            # Seção 5: Botões de Ação
            st.markdown("### ✅ Ações")
        
            col1, col2, col3 = st.columns([1, 1, 4])
        
            with col1:
                submit_button = st.form_submit_button(
                    "💾 Salvar Alterações",
                    use_container_width=True,
                    type="primary"
                )
            
            with col2:
                cancel_button = st.form_submit_button(
                    "❌ Cancelar",
                    use_container_width=True
                )
            
            # Processamento do formulário
            if submit_button:
                # Validações básicas
                if not nome_completo.strip():
                    st.error("❌ Nome completo é obrigatório!")
                    return
                
                if not cpf.strip():
                    st.error("❌ CPF é obrigatório!")
                    return
                
                if not validate_cpf(cpf):
                    st.error("❌ CPF inválido. Verifique o número!")
                    return
                
                if not data_nascimento:
                    st.error("❌ Data de nascimento é obrigatória!")
                    return
                
                if (date.today().year - data_nascimento.year) < 16 or (date.today().year - data_nascimento.year) > 100:
                    st.error("❌ O sócio deve ter entre 16 e 100 anos!")
                    return
                
                if not email.strip():
                    st.error("❌ Email é obrigatório!")
                    return
                
                if not validate_email(email):
                    st.error("❌ Email inválido. Verifique o formato!")
                    return
                
                if not telefone.strip():
                    st.error("❌ Telefone é obrigatório!")
                    return
                
                if not validate_phone(telefone):
                    st.error("❌ Telefone inválido. Use o formato (DD) 9XXXX-XXXX ou (DD) XXXX-XXXX!")
                    return
                
                if not comando_id:
                    st.error("❌ Comando é obrigatório!")
                    return
                
                # Validação opcional do CEP
                if cep and not validate_cep(cep):
                    st.error("❌ CEP inválido. Use o formato 00000-000!")
                    return
                
                # Processar dados
                cpf_limpo = ''.join(filter(str.isdigit, cpf))
                telefone_limpo = ''.join(filter(str.isdigit, telefone))
                
                # Processar dados de endereço
                cep_limpo = ''.join(filter(str.isdigit, cep)) if cep else None
                
                # Processar dados do plano
                plano_id_final = plano_id if plano_id != 0 else None
                
                # Calcular datas do plano se houver mudança
                data_adesao_plano = socio.get('data_adesao_plano')
                data_vencimento_plano = socio.get('data_vencimento_plano')
                
                if plano_id_final != socio.get('plano_id'):  # Plano mudou
                    if plano_id_final:
                        data_adesao_plano = date.today()
                        plano_info = db.execute_query_one("SELECT periodicidade FROM planos WHERE id = %s", (plano_id_final,))
                        if plano_info:
                            if plano_info['periodicidade'] == 'Mensal':
                                data_vencimento_plano = data_adesao_plano + timedelta(days=30)
                            elif plano_info['periodicidade'] == 'Trimestral':
                                data_vencimento_plano = data_adesao_plano + timedelta(days=90)
                            elif plano_info['periodicidade'] == 'Anual':
                                data_vencimento_plano = data_adesao_plano + timedelta(days=365)
                    else:  # Plano removido
                        data_adesao_plano = None
                        data_vencimento_plano = None
                
                # Processar nova foto
                foto_final = socio.get('foto')  # Manter foto atual por padrão
                if nova_foto_uploaded:
                    with st.spinner("Salvando nova foto..."):
                        nova_foto_path, error = save_socio_photo(nova_foto_uploaded, socio_id)
                        if error:
                            st.error(f"Erro ao salvar nova foto: {error}")
                            return
                        foto_final = nova_foto_path
                
                # Preparar dados de endereço
                endereco_data = {
                    'cep': cep_limpo,
                    'endereco': endereco.strip() if endereco else None,
                    'numero': numero.strip() if numero else None,
                    'complemento': complemento.strip() if complemento else None,
                    'bairro': bairro.strip() if bairro else None,
                    'cidade': cidade.strip() if cidade else None,
                    'estado': estado if estado else None
                }
                
                # Atualizar sócio
                if update_socio_complete(socio_id, nome_completo.strip(), cpf_limpo, data_nascimento, email.strip().lower(), telefone_limpo, tamanho_camisa, comando_id, foto_final, plano_id_final, data_adesao_plano, data_vencimento_plano, endereco_data):
                    show_success("✅ Sócio atualizado com sucesso!")
                    # Limpar cache
                    get_socios_data.clear()
                    get_report_data.clear()
                    st.session_state['socio_action'] = 'list'
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar sócio. Verifique os dados e tente novamente.")
            
            if cancel_button:
                st.session_state['socio_action'] = 'list'
                st.rerun()
    
    except Exception as e:
            st.error(f"Erro ao carregar formulário de edição: {e}")
            if st.button("⬅️ Voltar para a lista", key="btn_voltar_error_edit"):
                st.session_state['socio_action'] = 'list'
                st.rerun()

def show_report():
    """Mostrar relatório de sócios"""
    st.subheader("📊 Relatório de Sócios")
    
    # Botão para voltar
    if st.button("⬅️ Voltar", key="btn_voltar_report"):
        st.session_state['socio_action'] = 'list'
        st.rerun()
    
    st.markdown("---")
    
    # Buscar dados para relatório com cache
    with st.spinner("Gerando relatório..."):
        report_data = get_report_data()
    
    if report_data:
        # Resumo geral
        st.subheader("📈 Resumo Geral")
        total_socios = sum(item['total_socios'] for item in report_data)
        total_comandos = len([item for item in report_data if item['total_socios'] > 0])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Sócios", total_socios)
        with col2:
            st.metric("Comandos com Sócios", total_comandos)
        with col3:
            st.metric("Comandos Cadastrados", len(report_data))
        
        st.markdown("---")
        
        # Tabela detalhada
        st.subheader("📋 Relatório por Comando")
        df = pd.DataFrame(report_data)
        
        # Renomear colunas para melhor visualização
        df.columns = ['Comando', 'Total', 'PP', 'P', 'M', 'G', 'GG', 'XG', 'XXG']
        
        st.dataframe(df, use_container_width=True)
        
        # Gráfico de barras
        st.subheader("📊 Gráfico - Sócios por Comando")
        chart_data = df.set_index('Comando')['Total']
        st.bar_chart(chart_data)
        
        # Gráfico de pizza
        st.subheader("🥧 Distribuição por Comando")
        if total_socios > 0:
            # Filtrar apenas comandos com sócios
            chart_data_filtered = chart_data[chart_data > 0]
            if len(chart_data_filtered) > 0:
                # Usar plotly para gráfico de pizza
                import plotly.express as px
                fig = px.pie(values=chart_data_filtered.values, names=chart_data_filtered.index, title="Distribuição por Comando")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum sócio cadastrado para exibir gráfico de pizza.")
        else:
            st.info("Nenhum sócio cadastrado para exibir gráfico de pizza.")
        
        # Relatório de tamanhos
        st.subheader("👕 Distribuição por Tamanho de Camisa")
        tamanhos_data = {
            'PP': sum(item['tamanho_pp'] for item in report_data),
            'P': sum(item['tamanho_p'] for item in report_data),
            'M': sum(item['tamanho_m'] for item in report_data),
            'G': sum(item['tamanho_g'] for item in report_data),
            'GG': sum(item['tamanho_gg'] for item in report_data),
            'XG': sum(item['tamanho_xg'] for item in report_data),
            'XXG': sum(item['tamanho_xxg'] for item in report_data)
        }
        
        # Filtrar tamanhos com pelo menos 1 sócio
        tamanhos_filtered = {k: v for k, v in tamanhos_data.items() if v > 0}
        
        if tamanhos_filtered:
            col1, col2 = st.columns(2)
            
            with col1:
                st.bar_chart(tamanhos_filtered)
            
            with col2:
                # Usar plotly para gráfico de pizza de tamanhos
                import plotly.express as px
                fig = px.pie(values=list(tamanhos_filtered.values()), names=list(tamanhos_filtered.keys()), title="Distribuição por Tamanho")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum sócio cadastrado para exibir distribuição por tamanho.")
        
        # Relatório de planos
        st.subheader("🎫 Distribuição por Plano de Sócio")
        
        # Buscar dados de planos com cache
        planos_report_data = get_planos_report_data()
        
        if planos_report_data:
            # Criar DataFrame para planos
            df_planos = pd.DataFrame(planos_report_data)
            
            # Exibir tabela de planos
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Tabela de Planos**")
                # Preparar dados para exibição
                df_display_planos = df_planos[['plano_nome', 'total_socios', 'valor_plano', 'periodicidade']].copy()
                df_display_planos.columns = ['Plano', 'Sócios', 'Valor (R$)', 'Periodicidade']
                df_display_planos['Valor (R$)'] = df_display_planos['Valor (R$)'].apply(lambda x: f"R$ {x:.2f}" if x > 0 else "N/A")
                st.dataframe(df_display_planos, use_container_width=True)
            
            with col2:
                st.markdown("**📈 Gráfico de Planos**")
                
                # Preparar dados para gráfico
                planos_chart_data = df_planos.set_index('plano_nome')['total_socios']
                
                # Gráfico de barras
                st.bar_chart(planos_chart_data)
                
                # Gráfico de pizza se houver dados
                if planos_chart_data.sum() > 0:
                    fig_planos = px.pie(
                        values=planos_chart_data.values, 
                        names=planos_chart_data.index, 
                        title="Distribuição por Plano"
                    )
                    st.plotly_chart(fig_planos, use_container_width=True)
            
            # Estatísticas adicionais
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_com_plano = df_planos[df_planos['plano_nome'] != 'Sem Plano']['total_socios'].sum()
                st.metric("Sócios com Plano", total_com_plano)
            
            with col2:
                total_sem_plano = df_planos[df_planos['plano_nome'] == 'Sem Plano']['total_socios'].sum() if 'Sem Plano' in df_planos['plano_nome'].values else 0
                st.metric("Sócios sem Plano", total_sem_plano)
            
            with col3:
                percentual_com_plano = (total_com_plano / (total_com_plano + total_sem_plano) * 100) if (total_com_plano + total_sem_plano) > 0 else 0
                st.metric("Taxa de Adesão", f"{percentual_com_plano:.1f}%")
                
        else:
            st.info("Nenhum dado de plano encontrado para exibir relatório.")
        
        # Lista detalhada de sócios
        st.subheader("👥 Lista Detalhada de Sócios")
        socios_detalhados_query = """
        SELECT 
            s.nome_completo,
            s.cpf,
            s.email,
            s.telefone,
            s.data_nascimento,
            s.tamanho_camisa,
            c.nome as comando_nome,
            COALESCE(p.nome, 'Sem Plano') as plano_nome,
            COALESCE(p.valor, 0) as valor_plano,
            COALESCE(p.periodicidade, 'N/A') as periodicidade_plano
        FROM socios s
        LEFT JOIN comandos c ON s.comando_id = c.id
        LEFT JOIN planos p ON s.plano_id = p.id
        ORDER BY s.nome_completo
        """
        
        with st.spinner("Carregando lista detalhada..."):
            socios_detalhados = db.execute_query(socios_detalhados_query, fetch=True)
        
        if socios_detalhados:
            # Criar DataFrame para melhor visualização
            df_socios = pd.DataFrame(socios_detalhados)
            df_socios['CPF'] = df_socios['cpf'].apply(format_cpf)
            df_socios['Telefone'] = df_socios['telefone'].apply(format_phone)
            df_socios['Data Nascimento'] = df_socios['data_nascimento'].apply(format_date)
            
            # Preparar coluna de plano com valor formatado
            def format_plano(row):
                if row['valor_plano'] > 0:
                    return f"{row['plano_nome']} - R$ {row['valor_plano']:.2f} ({row['periodicidade_plano']})"
                else:
                    return row['plano_nome']
            
            df_socios['Plano Completo'] = df_socios.apply(format_plano, axis=1)
            
            # Selecionar e renomear colunas
            df_display = df_socios[['nome_completo', 'CPF', 'email', 'Telefone', 'Data Nascimento', 'tamanho_camisa', 'comando_nome', 'Plano Completo']].copy()
            df_display.columns = ['Nome', 'CPF', 'Email', 'Telefone', 'Data Nascimento', 'Tamanho Camisa', 'Comando', 'Plano']
            
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("Nenhum sócio cadastrado.")
    else:
        st.info("Nenhum dado encontrado para gerar o relatório.")

def validate_socio_form(nome, cpf, email, telefone, data_nascimento):
    """Validar formulário de sócio"""
    if not nome or not cpf or not email or not telefone or not data_nascimento:
        return False
    
    if not validate_cpf(cpf):
        st.error("CPF inválido!")
        return False
    
    if not validate_email(email):
        st.error("Email inválido!")
        return False
    
    if not validate_phone(telefone):
        st.error("Telefone inválido!")
        return False
    
    return True

def create_socio(nome, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id, foto, plano_id, endereco_data, data_cadastro=None):
    """Criar novo sócio"""
    try:
        # Verificar se CPF já existe
        cpf_check = "SELECT id FROM socios WHERE cpf = %s"
        existing = db.execute_query_one(cpf_check, (cpf,))
        
        if existing:
            st.error("CPF já cadastrado!")
            return False
        
        # Verificar se email já existe
        email_check = "SELECT id FROM socios WHERE email = %s"
        existing_email = db.execute_query_one(email_check, (email,))
        
        if existing_email:
            st.error("E-mail já cadastrado!")
            return False
        
        # Calcular datas do plano se houver
        data_adesao_plano = None
        data_vencimento_plano = None
        
        if plano_id:
            data_adesao_plano = date.today()
            # Buscar periodicidade do plano
            plano_info = db.execute_query_one("SELECT periodicidade FROM planos WHERE id = %s", (plano_id,))
            if plano_info:
                if plano_info['periodicidade'] == 'Mensal':
                    data_vencimento_plano = data_adesao_plano + timedelta(days=30)
                elif plano_info['periodicidade'] == 'Trimestral':
                    data_vencimento_plano = data_adesao_plano + timedelta(days=90)
                elif plano_info['periodicidade'] == 'Anual':
                    data_vencimento_plano = data_adesao_plano + timedelta(days=365)
        
        # Usar data fornecida ou data atual se não fornecida
        if data_cadastro is None:
            data_cadastro = date.today()
        
        # Inserir sócio
        insert_query = """
        INSERT INTO socios (nome_completo, foto, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id, 
                           plano_id, data_adesao_plano, data_vencimento_plano,
                           cep, endereco, numero, complemento, bairro, cidade, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (nome, foto, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id, 
                 plano_id, data_adesao_plano, data_vencimento_plano,
                 endereco_data['cep'], endereco_data['endereco'], endereco_data['numero'],
                 endereco_data['complemento'], endereco_data['bairro'], endereco_data['cidade'],
                 endereco_data['estado'])
        
        if db.execute_query(insert_query, params):
            return True
        else:
            return False
        
    except Exception as e:
        st.error(f"Erro ao criar sócio: {e}")
        return False

def update_socio(socio_id, nome, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id, foto):
    """Atualizar sócio"""
    try:
        # Verificar se CPF já existe em outro sócio
        cpf_check = "SELECT id FROM socios WHERE cpf = %s AND id != %s"
        existing = db.execute_query_one(cpf_check, (cpf, socio_id))
        
        if existing:
            st.error("CPF já cadastrado em outro sócio!")
            return False
        
        # Verificar se email já existe em outro sócio
        email_check = "SELECT id FROM socios WHERE email = %s AND id != %s"
        existing_email = db.execute_query_one(email_check, (email, socio_id))
        
        if existing_email:
            st.error("E-mail já cadastrado em outro sócio!")
            return False
        
        # Atualizar sócio
        update_query = """
        UPDATE socios 
        SET nome_completo = %s, cpf = %s, data_nascimento = %s, email = %s, 
            telefone = %s, tamanho_camisa = %s, comando_id = %s
        WHERE id = %s
        """
        
        params = (nome, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id, socio_id)
        
        if db.execute_query(update_query, params):
            return True
        else:
            return False
        
    except Exception as e:
        st.error(f"Erro ao atualizar sócio: {e}")
        return False

def update_socio_complete(socio_id, nome, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id, foto, plano_id, data_adesao_plano, data_vencimento_plano, endereco_data):
    """Atualizar sócio com todos os campos (versão completa)"""
    try:
        # Verificar se CPF já existe em outro sócio
        cpf_check = "SELECT id FROM socios WHERE cpf = %s AND id != %s"
        existing_cpf = db.execute_query_one(cpf_check, (cpf, socio_id))
        
        if existing_cpf:
            st.error("CPF já cadastrado para outro sócio!")
            return False
        
        # Verificar se Email já existe em outro sócio
        email_check = "SELECT id FROM socios WHERE email = %s AND id != %s"
        existing_email = db.execute_query_one(email_check, (email, socio_id))
        
        if existing_email:
            st.error("Email já cadastrado para outro sócio!")
            return False

        # Query completa com todos os campos
        update_query = """
        UPDATE socios 
        SET nome_completo = %s, foto = %s, cpf = %s, data_nascimento = %s, 
            email = %s, telefone = %s, tamanho_camisa = %s, comando_id = %s,
            plano_id = %s, data_adesao_plano = %s, data_vencimento_plano = %s,
            cep = %s, endereco = %s, numero = %s, complemento = %s, 
            bairro = %s, cidade = %s, estado = %s
        WHERE id = %s
        """
        
        params = (
            nome, foto, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id,
            plano_id, data_adesao_plano, data_vencimento_plano,
            endereco_data['cep'], endereco_data['endereco'], endereco_data['numero'],
            endereco_data['complemento'], endereco_data['bairro'], endereco_data['cidade'],
            endereco_data['estado'], socio_id
        )
        
        if db.execute_query(update_query, params):
            # Limpar cache
            get_socios_data.clear()
            get_report_data.clear()
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Erro ao atualizar sócio: {e}")
        return False

def delete_socio(socio_id):
    """Excluir sócio"""
    try:
        delete_query = "DELETE FROM socios WHERE id = %s"
        return db.execute_query(delete_query, (socio_id,))
    except Exception as e:
        st.error(f"Erro ao excluir sócio: {e}")
        return False