import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from config.database import db
from utils.helpers import format_currency, format_date, show_success, show_error

# Cache para planos
@st.cache_data(ttl=300)
def get_planos():
    """Buscar planos com cache"""
    try:
        planos_query = "SELECT * FROM planos WHERE ativo = TRUE ORDER BY valor"
        result = db.execute_query(planos_query, fetch=True)
        return result if result else []
    except Exception as e:
        st.error(f"Erro ao buscar planos: {e}")
        return []

@st.cache_data(ttl=60)
def get_socios_com_planos():
    """Buscar sócios com seus planos"""
    try:
        socios_query = """
        SELECT s.*, p.nome as plano_nome, p.valor as plano_valor, p.periodicidade,
               s.data_adesao_plano, s.data_vencimento_plano
        FROM socios s 
        LEFT JOIN planos p ON s.plano_id = p.id
        ORDER BY s.nome_completo
        """
        result = db.execute_query(socios_query, fetch=True)
        return result if result else []
    except Exception as e:
        st.error(f"Erro ao buscar sócios: {e}")
        return []

def show():
    st.title("🎫 Gestão de Planos")
    st.markdown("---")
    
    # Inicializar session_state se não existir
    if 'plano_action' not in st.session_state:
        st.session_state['plano_action'] = 'list'
    
    # Botões de ação
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("➕ Novo Plano", use_container_width=True, key="btn_novo_plano"):
            st.session_state['plano_action'] = 'create'
    
    with col2:
        if st.button("👥 Sócios com Planos", use_container_width=True, key="btn_socios_planos"):
            st.session_state['plano_action'] = 'socios'
    
    # Verificar ação e renderizar conteúdo
    action = st.session_state.get('plano_action', 'list')
    
    if action == 'create':
        show_create_form()
    elif action == 'edit':
        show_edit_form(st.session_state.get('plano_id'))
    elif action == 'socios':
        show_socios_planos()
    else:
        show_planos_list()

def show_planos_list():
    """Mostrar lista de planos"""
    
    st.subheader("📋 Planos Disponíveis")
    
    # Buscar planos com cache
    with st.spinner("Carregando planos..."):
        planos = get_planos()
    
    if planos:
        # Mostrar planos em cards
        cols = st.columns(len(planos))
        
        for idx, plano in enumerate(planos):
            with cols[idx]:
                with st.container():
                    # Determinar cor baseada no valor
                    if plano['valor'] <= 100:
                        border_color = "#CD7F32"  # Bronze
                        emoji = "🥉"
                    elif plano['valor'] <= 200:
                        border_color = "#C0C0C0"  # Prata
                        emoji = "🥈"
                    else:
                        border_color = "#FFD700"  # Ouro
                        emoji = "🥇"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #1a1a1a; 
                        padding: 1.5rem; 
                        border-radius: 0.5rem; 
                        border: 2px solid {border_color};
                        margin-bottom: 1rem;
                        text-align: center;
                    ">
                        <h2 style="color: {border_color}; margin: 0 0 10px 0;">{emoji} {plano['nome']}</h2>
                        <h3 style="color: #ffffff; margin: 0 0 10px 0;">{format_currency(plano['valor'])}</h3>
                        <p style="color: #888; margin: 0 0 15px 0; font-size: 0.9em;">{plano['periodicidade']}</p>
                        <div style="text-align: left; color: #ffffff; font-size: 0.8em;">
                    """, unsafe_allow_html=True)
                    
                    # Benefícios
                    beneficios = []
                    if plano['desconto_loja'] > 0:
                        beneficios.append(f"🛍️ {plano['desconto_loja']}% Loja")
                    if plano['desconto_caravanas'] > 0:
                        beneficios.append(f"🚌 {plano['desconto_caravanas']}% Caravanas")
                    if plano['desconto_bar'] > 0:
                        beneficios.append(f"🍺 {plano['desconto_bar']}% Bar")
                    if plano['inclui_camisa']:
                        beneficios.append(f"👕 {plano['camisa_tipo']}")
                    if plano['sorteio_mensal']:
                        beneficios.append("🎲 Sorteio Mensal")
                    if plano['grupo_exclusivo']:
                        beneficios.append("👥 Grupo Exclusivo")
                    
                    for beneficio in beneficios:
                        st.markdown(f"<div style='margin: 5px 0;'>{beneficio}</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
                    
                    # Botões de ação
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_{plano['id']}"):
                            st.session_state['plano_action'] = 'edit'
                            st.session_state['plano_id'] = plano['id']
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_{plano['id']}"):
                            if delete_plano(plano['id']):
                                show_success("Plano excluído com sucesso!")
                                get_planos.clear()
                                st.rerun()
                            else:
                                show_error("Erro ao excluir plano!")
        
        # Estatísticas
        st.markdown("---")
        st.subheader("📊 Estatísticas dos Planos")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Planos", len(planos))
        
        with col2:
            total_socios = db.execute_query("SELECT COUNT(*) as total FROM socios WHERE plano_id IS NOT NULL", fetch=True)
            total_socios = total_socios[0]['total'] if total_socios else 0
            st.metric("Sócios com Plano", total_socios)
        
        with col3:
            valor_medio = sum(p['valor'] for p in planos) / len(planos)
            st.metric("Valor Médio", format_currency(valor_medio))
        
        with col4:
            planos_ativos = len([p for p in planos if p['ativo']])
            st.metric("Planos Ativos", planos_ativos)
        
    else:
        st.info("Nenhum plano cadastrado ainda.")

def show_create_form():
    """Mostrar formulário de criação de plano"""
    
    # Header com botão voltar
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ Voltar", use_container_width=True, key="btn_voltar_create_plano"):
            st.session_state['plano_action'] = 'list'
            st.rerun()
    
    st.subheader("➕ Cadastro de Novo Plano")
    st.markdown("---")
    
    with st.form("create_plano_form", clear_on_submit=True):
        
        # Seção 1: Dados Básicos
        st.markdown("### 📋 Dados Básicos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do Plano *", placeholder="Ex: Sócio União Bronze")
            valor = st.number_input("Valor *", min_value=0.01, step=0.01, format="%.2f")
            periodicidade = st.selectbox(
                "Periodicidade *",
                ["Mensal", "Trimestral", "Anual"]
            )
        
        with col2:
            descricao = st.text_area("Descrição", placeholder="Descrição do plano e seus benefícios")
            ativo = st.checkbox("Plano Ativo", value=True)
        
        st.markdown("---")
        
        # Seção 2: Benefícios
        st.markdown("### 🎁 Benefícios")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            desconto_loja = st.number_input("Desconto Loja (%)", min_value=0, max_value=100, value=0)
            desconto_caravanas = st.number_input("Desconto Caravanas (%)", min_value=0, max_value=100, value=0)
        
        with col2:
            desconto_bar = st.number_input("Desconto Bar (%)", min_value=0, max_value=100, value=0)
            inclui_camisa = st.checkbox("Inclui Camisa")
        
        with col3:
            camisa_tipo = st.text_input("Tipo de Camisa", placeholder="Ex: Sócio União", disabled=not inclui_camisa)
            sorteio_mensal = st.checkbox("Sorteio Mensal")
        
        grupo_exclusivo = st.checkbox("Grupo Exclusivo", value=True)
        
        st.markdown("---")
        
        # Seção 3: Botões de Ação
        st.markdown("### ✅ Ações")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            submit_button = st.form_submit_button(
                "💾 Salvar Plano",
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
            if not nome.strip():
                st.error("❌ Nome do plano é obrigatório!")
                return
            
            if valor <= 0:
                st.error("❌ Valor deve ser maior que zero!")
                return
            
            if inclui_camisa and not camisa_tipo.strip():
                st.error("❌ Tipo de camisa é obrigatório quando 'Inclui Camisa' está marcado!")
                return
            
            # Processar dados
            plano_data = {
                'nome': nome.strip(),
                'descricao': descricao.strip() if descricao.strip() else None,
                'valor': valor,
                'periodicidade': periodicidade,
                'desconto_loja': desconto_loja,
                'desconto_caravanas': desconto_caravanas,
                'desconto_bar': desconto_bar,
                'inclui_camisa': inclui_camisa,
                'camisa_tipo': camisa_tipo.strip() if camisa_tipo.strip() else None,
                'sorteio_mensal': sorteio_mensal,
                'grupo_exclusivo': grupo_exclusivo,
                'ativo': ativo
            }
            
            # Salvar no banco
            if create_plano(plano_data):
                show_success("✅ Plano criado com sucesso!")
                # Limpar cache
                get_planos.clear()
                get_socios_com_planos.clear()
                st.session_state['plano_action'] = 'list'
                st.rerun()
            else:
                show_error("❌ Erro ao criar plano!")
        
        elif cancel_button:
            st.session_state['plano_action'] = 'list'
            st.rerun()

def show_edit_form(plano_id):
    """Mostrar formulário de edição de plano"""
    
    if not plano_id:
        st.error("ID do plano não encontrado!")
        return
    
    # Buscar dados do plano
    plano_query = "SELECT * FROM planos WHERE id = %s"
    plano = db.execute_query_one(plano_query, (plano_id,))
    
    if not plano:
        st.error("Plano não encontrado!")
        return
    
    st.subheader("✏️ Editar Plano")
    
    # Botão para voltar
    if st.button("⬅️ Voltar", key="btn_voltar_edit_plano"):
        st.session_state['plano_action'] = 'list'
        st.rerun()
    
    with st.form("edit_plano_form"):
        
        # Seção 1: Dados Básicos
        st.markdown("### 📋 Dados Básicos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do Plano *", value=plano['nome'])
            valor = st.number_input("Valor *", value=float(plano['valor']), min_value=0.01, step=0.01, format="%.2f")
            periodicidade = st.selectbox(
                "Periodicidade *",
                ["Mensal", "Trimestral", "Anual"],
                index=["Mensal", "Trimestral", "Anual"].index(plano['periodicidade'])
            )
        
        with col2:
            descricao = st.text_area("Descrição", value=plano['descricao'] or "")
            ativo = st.checkbox("Plano Ativo", value=plano['ativo'])
        
        st.markdown("---")
        
        # Seção 2: Benefícios
        st.markdown("### 🎁 Benefícios")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            desconto_loja = st.number_input("Desconto Loja (%)", min_value=0, max_value=100, value=plano['desconto_loja'])
            desconto_caravanas = st.number_input("Desconto Caravanas (%)", min_value=0, max_value=100, value=plano['desconto_caravanas'])
        
        with col2:
            desconto_bar = st.number_input("Desconto Bar (%)", min_value=0, max_value=100, value=plano['desconto_bar'])
            inclui_camisa = st.checkbox("Inclui Camisa", value=plano['inclui_camisa'])
        
        with col3:
            camisa_tipo = st.text_input("Tipo de Camisa", value=plano['camisa_tipo'] or "", disabled=not inclui_camisa)
            sorteio_mensal = st.checkbox("Sorteio Mensal", value=plano['sorteio_mensal'])
        
        grupo_exclusivo = st.checkbox("Grupo Exclusivo", value=plano['grupo_exclusivo'])
        
        st.markdown("---")
        
        # Seção 3: Botões de Ação
        st.markdown("### ✅ Ações")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            submit_button = st.form_submit_button(
                "💾 Atualizar Plano",
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
            if not nome.strip():
                st.error("❌ Nome do plano é obrigatório!")
                return
            
            if valor <= 0:
                st.error("❌ Valor deve ser maior que zero!")
                return
            
            if inclui_camisa and not camisa_tipo.strip():
                st.error("❌ Tipo de camisa é obrigatório quando 'Inclui Camisa' está marcado!")
                return
            
            # Processar dados
            plano_data = {
                'nome': nome.strip(),
                'descricao': descricao.strip() if descricao.strip() else None,
                'valor': valor,
                'periodicidade': periodicidade,
                'desconto_loja': desconto_loja,
                'desconto_caravanas': desconto_caravanas,
                'desconto_bar': desconto_bar,
                'inclui_camisa': inclui_camisa,
                'camisa_tipo': camisa_tipo.strip() if camisa_tipo.strip() else None,
                'sorteio_mensal': sorteio_mensal,
                'grupo_exclusivo': grupo_exclusivo,
                'ativo': ativo
            }
            
            # Salvar no banco
            if update_plano(plano_id, plano_data):
                show_success("✅ Plano atualizado com sucesso!")
                # Limpar cache
                get_planos.clear()
                get_socios_com_planos.clear()
                st.session_state['plano_action'] = 'list'
                st.rerun()
            else:
                show_error("❌ Erro ao atualizar plano!")
        
        elif cancel_button:
            st.session_state['plano_action'] = 'list'
            st.rerun()

def show_socios_planos():
    """Mostrar sócios com seus planos"""
    
    st.subheader("👥 Sócios com Planos")
    
    # Botão para voltar
    if st.button("⬅️ Voltar", key="btn_voltar_socios_planos"):
        st.session_state['plano_action'] = 'list'
        st.rerun()
    
    st.markdown("---")
    
    # Buscar sócios com planos
    with st.spinner("Carregando sócios com planos..."):
        socios = get_socios_com_planos()
    
    if socios:
        # Filtros
        st.subheader("🔍 Filtros")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            planos = get_planos()
            plano_options = {0: "Todos os planos"}
            plano_options.update({p['id']: p['nome'] for p in planos})
            
            plano_filtro = st.selectbox(
                "Filtrar por Plano",
                options=list(plano_options.keys()),
                format_func=lambda x: plano_options[x]
            )
        
        with col2:
            status_filtro = st.selectbox(
                "Status do Plano",
                ["Todos", "Ativos", "Vencidos", "Sem Plano"]
            )
        
        with col3:
            search_term = st.text_input("Buscar por nome")
        
        # Aplicar filtros
        filtered_socios = []
        for socio in socios:
            match_plano = (plano_filtro == 0) or (socio['plano_id'] == plano_filtro)
            match_search = (not search_term) or (search_term.lower() in socio['nome_completo'].lower())
            
            # Status do plano
            match_status = True
            if status_filtro == "Ativos":
                match_status = socio['plano_id'] and socio['data_vencimento_plano'] and socio['data_vencimento_plano'] >= date.today()
            elif status_filtro == "Vencidos":
                match_status = socio['plano_id'] and socio['data_vencimento_plano'] and socio['data_vencimento_plano'] < date.today()
            elif status_filtro == "Sem Plano":
                match_status = not socio['plano_id']
            
            if match_plano and match_search and match_status:
                filtered_socios.append(socio)
        
        # Mostrar resultados
        if filtered_socios:
            st.subheader(f"📋 Resultados ({len(filtered_socios)} sócios)")
            
            for socio in filtered_socios:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**{socio['nome_completo']}**")
                        st.write(f"📧 {socio['email']}")
                    
                    with col2:
                        if socio['plano_nome']:
                            st.write(f"🎫 {socio['plano_nome']}")
                            st.write(f"💰 {format_currency(socio['plano_valor'])} - {socio['periodicidade']}")
                        else:
                            st.write("❌ Sem plano")
                    
                    with col3:
                        if socio['data_adesao_plano']:
                            st.write(f"📅 Adesão: {format_date(socio['data_adesao_plano'])}")
                        if socio['data_vencimento_plano']:
                            vencimento = socio['data_vencimento_plano']
                            if vencimento < date.today():
                                st.error(f"⚠️ Vencido: {format_date(vencimento)}")
                            elif vencimento <= date.today() + timedelta(days=30):
                                st.warning(f"⏰ Vence: {format_date(vencimento)}")
                            else:
                                st.write(f"✅ Vence: {format_date(vencimento)}")
                    
                    with col4:
                        if st.button("✏️", key=f"edit_plano_{socio['id']}"):
                            st.session_state['socio_action'] = 'edit'
                            st.session_state['socio_id'] = socio['id']
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("Nenhum sócio encontrado com os filtros aplicados.")
    else:
        st.info("Nenhum sócio cadastrado.")

def create_plano(plano_data):
    """Criar novo plano"""
    try:
        insert_query = """
        INSERT INTO planos (nome, descricao, valor, periodicidade, desconto_loja, 
                           desconto_caravanas, desconto_bar, inclui_camisa, camisa_tipo, 
                           sorteio_mensal, grupo_exclusivo, ativo)
        VALUES (%(nome)s, %(descricao)s, %(valor)s, %(periodicidade)s, %(desconto_loja)s,
                %(desconto_caravanas)s, %(desconto_bar)s, %(inclui_camisa)s, %(camisa_tipo)s,
                %(sorteio_mensal)s, %(grupo_exclusivo)s, %(ativo)s)
        """
        
        return db.execute_query(insert_query, plano_data)
        
    except Exception as e:
        st.error(f"Erro ao criar plano: {e}")
        return False

def update_plano(plano_id, plano_data):
    """Atualizar plano"""
    try:
        update_query = """
        UPDATE planos 
        SET nome = %(nome)s, descricao = %(descricao)s, valor = %(valor)s, 
            periodicidade = %(periodicidade)s, desconto_loja = %(desconto_loja)s,
            desconto_caravanas = %(desconto_caravanas)s, desconto_bar = %(desconto_bar)s,
            inclui_camisa = %(inclui_camisa)s, camisa_tipo = %(camisa_tipo)s,
            sorteio_mensal = %(sorteio_mensal)s, grupo_exclusivo = %(grupo_exclusivo)s,
            ativo = %(ativo)s
        WHERE id = %s
        """
        
        plano_data['id'] = plano_id
        return db.execute_query(update_query, plano_data)
        
    except Exception as e:
        st.error(f"Erro ao atualizar plano: {e}")
        return False

def delete_plano(plano_id):
    """Excluir plano (desativar)"""
    try:
        # Verificar se há sócios usando este plano
        check_socios = db.execute_query("SELECT COUNT(*) as total FROM socios WHERE plano_id = %s", (plano_id,), fetch=True)
        if check_socios and check_socios[0]['total'] > 0:
            st.error("Não é possível excluir plano que possui sócios associados!")
            return False
        
        # Desativar plano em vez de excluir
        update_query = "UPDATE planos SET ativo = FALSE WHERE id = %s"
        return db.execute_query(update_query, (plano_id,))
        
    except Exception as e:
        st.error(f"Erro ao excluir plano: {e}")
        return False

