import streamlit as st
import pandas as pd
from datetime import datetime, date
from config.database import db
from utils.helpers import create_metric_card, format_currency, format_date

def show():
    st.title("🏠 Dashboard")
    st.markdown("---")
    
    # Buscar dados do dashboard
    dashboard_data = get_dashboard_data()
    
    # Cards de métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "Total de Sócios",
            dashboard_data['total_socios'],
            "sócios cadastrados"
        )
    
    with col2:
        create_metric_card(
            "Faturas Pagas",
            format_currency(dashboard_data['valor_total']),
            f"{dashboard_data['total_faturas']} faturas"
        )
    
    with col3:
        create_metric_card(
            "Faturas em Atraso",
            dashboard_data['faturas_atrasadas'],
            "precisam de atenção"
        )
    
    st.markdown("---")
    
    # Ranking de Comandos
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏆 Ranking de Comandos")
        ranking_df = pd.DataFrame(dashboard_data['ranking_comandos'])
        if not ranking_df.empty:
            st.dataframe(
                ranking_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhum comando cadastrado ainda.")
    
    with col2:
        st.subheader("📊 Resumo Mensal")
        st.metric(
            "Recebido este mês",
            format_currency(dashboard_data['valor_mes_atual'])
        )
        st.metric(
            "Faturas do mês",
            dashboard_data['faturas_mes_atual']
        )
    
    # Faturas em Atraso
    if dashboard_data['faturas_atrasadas_list']:
        st.markdown("---")
        st.subheader("⚠️ Faturas em Atraso")
        
        faturas_df = pd.DataFrame(dashboard_data['faturas_atrasadas_list'])
        faturas_df['data_vencimento'] = pd.to_datetime(faturas_df['data_vencimento']).dt.strftime('%d/%m/%Y')
        faturas_df['valor'] = faturas_df['valor'].apply(lambda x: format_currency(x))
        
        st.dataframe(
            faturas_df[['socio_nome', 'comando_nome', 'data_vencimento', 'valor', 'dias_atraso']],
            use_container_width=True,
            hide_index=True
        )

def get_dashboard_data():
    """Buscar dados para o dashboard"""
    
    # Total de sócios
    total_socios_query = "SELECT COUNT(*) as total FROM socios"
    total_socios_result = db.execute_query_one(total_socios_query)
    total_socios = total_socios_result['total'] if total_socios_result else 0
    
    # Faturas pagas
    faturas_pagas_query = """
    SELECT 
        COUNT(*) as total_faturas, 
        SUM(valor) as valor_total,
        COUNT(CASE WHEN MONTH(data_pagamento) = MONTH(CURRENT_DATE) 
                   AND YEAR(data_pagamento) = YEAR(CURRENT_DATE) THEN 1 END) as faturas_mes_atual,
        SUM(CASE WHEN MONTH(data_pagamento) = MONTH(CURRENT_DATE) 
                 AND YEAR(data_pagamento) = YEAR(CURRENT_DATE) THEN valor ELSE 0 END) as valor_mes_atual
    FROM faturas 
    WHERE status = 'Pago'
    """
    faturas_pagas_result = db.execute_query_one(faturas_pagas_query)
    
    # Ranking de comandos
    ranking_query = """
    SELECT c.nome, COUNT(s.id) as total_socios 
    FROM comandos c 
    LEFT JOIN socios s ON s.comando_id = c.id 
    GROUP BY c.id, c.nome 
    ORDER BY total_socios DESC
    """
    ranking_result = db.execute_query(ranking_query, fetch=True)
    
    # Faturas em atraso
    faturas_atrasadas_query = """
    SELECT f.*, s.nome_completo as socio_nome, c.nome as comando_nome,
           DATEDIFF(CURRENT_DATE, f.data_vencimento) as dias_atraso
    FROM faturas f 
    INNER JOIN socios s ON f.socio_id = s.id 
    INNER JOIN comandos c ON f.comando_id = c.id 
    WHERE (f.status = 'Pendente' AND f.data_vencimento < CURRENT_DATE)
       OR f.status = 'Atrasado'
    ORDER BY f.data_vencimento ASC
    """
    faturas_atrasadas_result = db.execute_query(faturas_atrasadas_query, fetch=True)
    
    return {
        'total_socios': total_socios,
        'total_faturas': faturas_pagas_result['total_faturas'] if faturas_pagas_result else 0,
        'valor_total': faturas_pagas_result['valor_total'] if faturas_pagas_result else 0,
        'faturas_mes_atual': faturas_pagas_result['faturas_mes_atual'] if faturas_pagas_result else 0,
        'valor_mes_atual': faturas_pagas_result['valor_mes_atual'] if faturas_pagas_result else 0,
        'ranking_comandos': ranking_result or [],
        'faturas_atrasadas': len(faturas_atrasadas_result) if faturas_atrasadas_result else 0,
        'faturas_atrasadas_list': faturas_atrasadas_result or []
    }
