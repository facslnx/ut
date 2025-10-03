import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from config.database import db
from utils.helpers import format_currency, format_date, show_success, show_error

def show():
    st.title("💰 Gestão de Faturas")
    st.markdown("---")
    
    # Inicializar session_state se não existir
    if 'fatura_action' not in st.session_state:
        st.session_state['fatura_action'] = 'list'
    
    # Botões de ação
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("➕ Nova Fatura", use_container_width=True, key="btn_nova_fatura"):
            st.session_state['fatura_action'] = 'create'
    
    with col2:
        if st.button("📊 Relatório", use_container_width=True, key="btn_relatorio_faturas"):
            st.session_state['fatura_action'] = 'report'
    
    # Verificar ação e renderizar conteúdo
    action = st.session_state.get('fatura_action', 'list')
    
    if action == 'create':
        show_create_form()
    elif action == 'edit':
        show_edit_form(st.session_state.get('fatura_id'))
    elif action == 'report':
        show_report()
    else:
        show_faturas_list()

def show_faturas_list():
    """Mostrar lista de faturas"""
    
    # Filtros
    st.subheader("🔍 Filtros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Buscar comandos para filtro
        comandos_query = "SELECT id, nome FROM comandos ORDER BY nome"
        comandos = db.execute_query(comandos_query, fetch=True)
        comando_options = {0: "Todos os comandos"}
        comando_options.update({c['id']: c['nome'] for c in comandos})
        
        comando_filtro = st.selectbox(
            "Filtrar por Comando",
            options=list(comando_options.keys()),
            format_func=lambda x: comando_options[x]
        )
    
    with col2:
        status_filtro = st.selectbox(
            "Status",
            ["Todos", "Pendente", "Pago", "Atrasado"]
        )
    
    with col3:
        periodo = st.selectbox(
            "Período",
            ["Todos", "Este mês", "Últimos 3 meses", "Este ano"]
        )
    
    # Buscar faturas
    faturas_query = """
    SELECT f.*, s.nome_completo as socio_nome, s.cpf as socio_cpf, c.nome as comando_nome,
           DATEDIFF(CURRENT_DATE, f.data_vencimento) as dias_atraso
    FROM faturas f 
    INNER JOIN socios s ON f.socio_id = s.id 
    INNER JOIN comandos c ON f.comando_id = c.id
    WHERE 1=1
    """
    params = []
    
    if comando_filtro != 0:
        faturas_query += " AND f.comando_id = %s"
        params.append(comando_filtro)
    
    if status_filtro != "Todos":
        faturas_query += " AND f.status = %s"
        params.append(status_filtro)
    
    if periodo == "Este mês":
        faturas_query += " AND MONTH(f.data_vencimento) = MONTH(CURRENT_DATE) AND YEAR(f.data_vencimento) = YEAR(CURRENT_DATE)"
    elif periodo == "Últimos 3 meses":
        faturas_query += " AND f.data_vencimento >= DATE_SUB(CURRENT_DATE, INTERVAL 3 MONTH)"
    elif periodo == "Este ano":
        faturas_query += " AND YEAR(f.data_vencimento) = YEAR(CURRENT_DATE)"
    
    faturas_query += " ORDER BY f.data_vencimento DESC"
    
    faturas = db.execute_query(faturas_query, params, fetch=True)
    
    if faturas:
        # Mostrar tabela
        st.subheader("📋 Lista de Faturas")
        
        # Mostrar cada fatura em um card
        for fatura in faturas:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                
                with col1:
                    st.write(f"**{fatura['socio_nome']}**")
                    st.write(f"🏛️ {fatura['comando_nome']}")
                
                with col2:
                    st.write(f"📅 Vencimento: {format_date(fatura['data_vencimento'])}")
                    if fatura['data_pagamento']:
                        st.write(f"✅ Pago em: {format_date(fatura['data_pagamento'])}")
                
                with col3:
                    st.write(f"💰 {format_currency(fatura['valor'])}")
                    if fatura['forma_pagamento']:
                        st.write(f"💳 {fatura['forma_pagamento']}")
                
                with col4:
                    # Status com cores
                    status = fatura['status']
                    if status == 'Pago':
                        st.success(f"✅ {status}")
                    elif status == 'Atrasado':
                        st.error(f"❌ {status} ({fatura['dias_atraso']} dias)")
                    else:
                        st.warning(f"⏳ {status}")
                
                with col5:
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️", key=f"edit_{fatura['id']}"):
                            st.session_state['fatura_action'] = 'edit'
                            st.session_state['fatura_id'] = fatura['id']
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_{fatura['id']}"):
                            if delete_fatura(fatura['id']):
                                show_success("Fatura excluída com sucesso!")
                                st.rerun()
                            else:
                                show_error("Erro ao excluir fatura!")
                
                st.markdown("---")
    else:
        st.info("Nenhuma fatura encontrada com os filtros aplicados.")

def show_create_form():
    """Mostrar formulário de criação"""
    st.subheader("➕ Nova Fatura")
    
    with st.form("create_fatura_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Buscar sócios
            socios_query = "SELECT id, nome_completo FROM socios ORDER BY nome_completo"
            socios = db.execute_query(socios_query, fetch=True)
            socio_options = {s['id']: s['nome_completo'] for s in socios}
            socio_id = st.selectbox(
                "Sócio *",
                options=list(socio_options.keys()),
                format_func=lambda x: socio_options[x]
            )
            
            # Buscar comandos
            comandos_query = "SELECT id, nome FROM comandos ORDER BY nome"
            comandos = db.execute_query(comandos_query, fetch=True)
            comando_options = {c['id']: c['nome'] for c in comandos}
            comando_id = st.selectbox(
                "Comando *",
                options=list(comando_options.keys()),
                format_func=lambda x: comando_options[x]
            )
            
            valor = st.number_input("Valor *", value=150.00, min_value=0.01, step=0.01)
        
        with col2:
            data_vencimento = st.date_input("Data de Vencimento *")
            data_renovacao = st.date_input("Data de Renovação *")
            forma_pagamento = st.selectbox(
                "Forma de Pagamento",
                ["A vista", "Parcelado no Cartão", "Dinheiro", "Cartão a vista", "PIX", "Em mãos"]
            )
            
            comprovante = st.file_uploader("Comprovante (opcional)", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.form_submit_button("💾 Salvar", use_container_width=True):
                if validate_fatura_form(socio_id, comando_id, data_vencimento, data_renovacao, valor):
                    if create_fatura(socio_id, comando_id, valor, data_vencimento, data_renovacao, forma_pagamento, comprovante):
                        show_success("Fatura criada com sucesso!")
                        st.session_state['fatura_action'] = 'list'
                        st.rerun()
                    else:
                        show_error("Erro ao criar fatura!")
                else:
                    show_error("Por favor, preencha todos os campos obrigatórios!")
        
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state['fatura_action'] = 'list'
                st.rerun()

def show_edit_form(fatura_id):
    """Mostrar formulário de edição"""
    st.subheader("✏️ Editar Fatura")
    
    # Buscar dados da fatura
    fatura_query = "SELECT * FROM faturas WHERE id = %s"
    fatura = db.execute_query_one(fatura_query, (fatura_id,))
    
    if not fatura:
        show_error("Fatura não encontrada!")
        st.session_state['fatura_action'] = 'list'
        st.rerun()
        return
    
    with st.form("edit_fatura_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Buscar sócios
            socios_query = "SELECT id, nome_completo FROM socios ORDER BY nome_completo"
            socios = db.execute_query(socios_query, fetch=True)
            socio_options = {s['id']: s['nome_completo'] for s in socios}
            socio_id = st.selectbox(
                "Sócio *",
                options=list(socio_options.keys()),
                format_func=lambda x: socio_options[x],
                index=list(socio_options.keys()).index(fatura['socio_id'])
            )
            
            # Buscar comandos
            comandos_query = "SELECT id, nome FROM comandos ORDER BY nome"
            comandos = db.execute_query(comandos_query, fetch=True)
            comando_options = {c['id']: c['nome'] for c in comandos}
            comando_id = st.selectbox(
                "Comando *",
                options=list(comando_options.keys()),
                format_func=lambda x: comando_options[x],
                index=list(comando_options.keys()).index(fatura['comando_id'])
            )
            
            valor = st.number_input("Valor *", value=float(fatura['valor']), min_value=0.01, step=0.01)
            
            data_vencimento = st.date_input("Data de Vencimento *", value=fatura['data_vencimento'])
            data_renovacao = st.date_input("Data de Renovação *", value=fatura['data_renovacao'])
        
        with col2:
            data_pagamento = st.date_input("Data de Pagamento", value=fatura['data_pagamento'])
            
            status = st.selectbox(
                "Status",
                ["Pendente", "Pago", "Atrasado"],
                index=["Pendente", "Pago", "Atrasado"].index(fatura['status'])
            )
            
            forma_pagamento = st.selectbox(
                "Forma de Pagamento",
                ["A vista", "Parcelado no Cartão", "Dinheiro", "Cartão a vista", "PIX", "Em mãos"],
                index=["A vista", "Parcelado no Cartão", "Dinheiro", "Cartão a vista", "PIX", "Em mãos"].index(fatura['forma_pagamento']) if fatura['forma_pagamento'] else 0
            )
            
            comprovante = st.file_uploader("Novo Comprovante (opcional)", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.form_submit_button("💾 Salvar", use_container_width=True):
                if validate_fatura_form(socio_id, comando_id, data_vencimento, data_renovacao, valor):
                    if update_fatura(fatura_id, socio_id, comando_id, valor, data_vencimento, data_renovacao, data_pagamento, status, forma_pagamento, comprovante):
                        show_success("Fatura atualizada com sucesso!")
                        st.session_state['fatura_action'] = 'list'
                        st.rerun()
                    else:
                        show_error("Erro ao atualizar fatura!")
                else:
                    show_error("Por favor, preencha todos os campos obrigatórios!")
        
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state['fatura_action'] = 'list'
                st.rerun()

def show_report():
    """Mostrar relatório de faturas"""
    st.subheader("📊 Relatório de Faturas")
    
    # Buscar dados para relatório
    report_query = """
    SELECT 
        c.nome as comando,
        COUNT(f.id) as total_faturas,
        SUM(f.valor) as valor_total,
        COUNT(CASE WHEN f.status = 'Pago' THEN 1 END) as faturas_pagas,
        SUM(CASE WHEN f.status = 'Pago' THEN f.valor ELSE 0 END) as valor_pago,
        COUNT(CASE WHEN f.status = 'Atrasado' THEN 1 END) as faturas_atrasadas
    FROM comandos c
    LEFT JOIN faturas f ON c.id = f.comando_id
    GROUP BY c.id, c.nome
    ORDER BY valor_total DESC
    """
    
    report_data = db.execute_query(report_query, fetch=True)
    
    if report_data:
        df = pd.DataFrame(report_data)
        df['valor_total'] = df['valor_total'].apply(lambda x: format_currency(x) if x else "R$ 0,00")
        df['valor_pago'] = df['valor_pago'].apply(lambda x: format_currency(x) if x else "R$ 0,00")
        
        st.dataframe(df, use_container_width=True)
        
        # Gráfico
        st.subheader("📈 Gráfico por Comando")
        chart_data = df[['comando', 'total_faturas', 'faturas_pagas', 'faturas_atrasadas']].copy()
        chart_data = chart_data.set_index('comando')
        st.bar_chart(chart_data)
    else:
        st.info("Nenhum dado encontrado para o relatório.")

def validate_fatura_form(socio_id, comando_id, data_vencimento, data_renovacao, valor):
    """Validar formulário de fatura"""
    return socio_id and comando_id and data_vencimento and data_renovacao and valor

def create_fatura(socio_id, comando_id, valor, data_vencimento, data_renovacao, forma_pagamento, comprovante):
    """Criar nova fatura"""
    try:
        insert_query = """
        INSERT INTO faturas (socio_id, comando_id, valor, data_vencimento, data_renovacao, forma_pagamento)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (socio_id, comando_id, valor, data_vencimento, data_renovacao, forma_pagamento)
        
        if db.execute_query(insert_query, params):
            # TODO: Salvar comprovante se fornecido
            return True
        return False
        
    except Exception as e:
        show_error(f"Erro ao criar fatura: {e}")
        return False

def update_fatura(fatura_id, socio_id, comando_id, valor, data_vencimento, data_renovacao, data_pagamento, status, forma_pagamento, comprovante):
    """Atualizar fatura"""
    try:
        update_query = """
        UPDATE faturas 
        SET socio_id = %s, comando_id = %s, valor = %s, data_vencimento = %s, 
            data_renovacao = %s, data_pagamento = %s, status = %s, forma_pagamento = %s
        WHERE id = %s
        """
        
        params = (socio_id, comando_id, valor, data_vencimento, data_renovacao, 
                 data_pagamento, status, forma_pagamento, fatura_id)
        
        return db.execute_query(update_query, params)
        
    except Exception as e:
        show_error(f"Erro ao atualizar fatura: {e}")
        return False

def delete_fatura(fatura_id):
    """Excluir fatura"""
    try:
        delete_query = "DELETE FROM faturas WHERE id = %s"
        return db.execute_query(delete_query, (fatura_id,))
    except Exception as e:
        show_error(f"Erro ao excluir fatura: {e}")
        return False
