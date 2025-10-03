import streamlit as st
import pandas as pd
from config.database import db
from utils.helpers import show_success, show_error, format_date
from utils.validators import validate_cpf, validate_email, validate_phone, format_cpf, format_phone, validate_cep, format_cep
from utils.photo_manager import create_photo_upload_widget, save_socio_photo
from datetime import date, timedelta
import time

# Cache para comandos
@st.cache_data(ttl=300)
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
@st.cache_data(ttl=300)
def get_planos():
    """Buscar planos com cache"""
    try:
        # Verificar se a tabela planos existe
        check_table = "SHOW TABLES LIKE 'planos'"
        table_exists = db.execute_query(check_table, fetch=True)
        
        if not table_exists:
            st.warning("Tabela de planos não encontrada.")
            return []
        
        planos_query = "SELECT * FROM planos WHERE ativo = TRUE ORDER BY valor"
        result = db.execute_query(planos_query, fetch=True)
        
        if result:
            return result
        else:
            # Se não há planos ativos, buscar todos
            planos_query_all = "SELECT * FROM planos ORDER BY valor"
            result_all = db.execute_query(planos_query_all, fetch=True)
            return result_all if result_all else []
            
    except Exception as e:
        print(f"Erro ao buscar planos: {e}")
        return []

def create_socio_publico(nome, cpf, data_nascimento, email, telefone, tamanho_camisa, comando_id, foto, plano_id, endereco_data):
    """Criar novo sócio via cadastro público"""
    try:
        # Verificar se CPF já existe
        cpf_check = "SELECT id FROM socios WHERE cpf = %s"
        existing = db.execute_query_one(cpf_check, (cpf,))
        
        if existing:
            return False, "CPF já cadastrado!"
        
        # Verificar se email já existe
        email_check = "SELECT id FROM socios WHERE email = %s"
        existing_email = db.execute_query_one(email_check, (email,))
        
        if existing_email:
            return False, "E-mail já cadastrado!"
        
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
            return True, "Sócio cadastrado com sucesso!"
        else:
            return False, "Erro ao cadastrar sócio"
            
    except Exception as e:
        return False, f"Erro ao criar sócio: {e}"

def show_planos_cards():
    """Mostrar cards dos planos de forma atrativa"""
    try:
        planos = get_planos()
        
        if not planos:
            st.warning("⚠️ Nenhum plano disponível no momento.")
            st.info("Entre em contato conosco para mais informações sobre os planos.")
            return None
        
        # Verificar se todos os planos têm os campos necessários
        planos_validos = []
        for plano in planos:
            if all(key in plano for key in ['id', 'nome', 'valor', 'periodicidade']):
                planos_validos.append(plano)
            else:
                st.warning(f"Plano '{plano.get('nome', 'Desconhecido')}' tem dados incompletos.")
        
        if not planos_validos:
            st.error("❌ Nenhum plano válido encontrado.")
            return None
        
        planos = planos_validos
        
        st.markdown("### 🎫 Escolha seu Plano de Sócio")
        st.markdown("Selecione o plano que melhor se adequa ao seu perfil:")
        
        # Cores para os cards
        colors = {
            'Bronze': '#CD7F32',
            'Prata': '#C0C0C0', 
            'Ouro': '#FFD700'
        }
        
        # Layout responsivo com colunas
        if len(planos) == 1:
            cols = st.columns(1)
        elif len(planos) == 2:
            cols = st.columns(2)
        else:
            cols = st.columns(3)
        
        plano_selecionado = None
        
        for idx, plano in enumerate(planos):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                # Determinar cor baseada no nome
                plano_nome = plano['nome'].split()[-1] if ' ' in plano['nome'] else plano['nome']
                card_color = colors.get(plano_nome, '#1a1a1a')
                
                # Verificar se este plano está selecionado
                plano_selecionado = st.session_state.get('plano_selecionado')
                is_selected = plano_selecionado == plano['id']
                
                # Definir estilo baseado na seleção
                if is_selected:
                    border_style = f"4px solid {card_color}; box-shadow: 0 0 20px {card_color}40;"
                    bg_style = f"background: linear-gradient(135deg, {card_color}30, {card_color}50);"
                    selected_indicator = "✅ SELECIONADO"
                else:
                    border_style = f"2px solid {card_color};"
                    bg_style = "background-color: #1a1a1a;"
                    selected_indicator = "🔘 Clique para selecionar"
                
                # Card do plano
                with st.container():
                    st.markdown(f"""
                    <div style="
                        {bg_style}
                        border: {border_style}
                        border-radius: 15px;
                        padding: 20px;
                        margin: 10px 0;
                        text-align: center;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        position: relative;
                    ">
                        <div style="position: absolute; top: 10px; right: 15px; font-size: 0.8em; color: {card_color}; font-weight: bold;">
                            {selected_indicator}
                        </div>
                        <h3 style="color: {card_color}; margin: 25px 0 10px 0; font-size: 1.5em;">
                            {plano['nome']}
                        </h3>
                        <div style="font-size: 2.2em; font-weight: bold; color: {card_color}; margin: 15px 0;">
                            R$ {plano['valor']:.2f}
                        </div>
                        <div style="color: #888; margin-bottom: 20px; font-size: 1.1em;">
                            {plano['periodicidade']}
                        </div>
                        <hr style="border: 1px solid {card_color}; margin: 15px 0;">
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar benefícios em uma lista compacta
                    beneficios = []
                    beneficios.append(f"🛍️ {plano.get('desconto_loja', 0)}% Loja União")
                    beneficios.append(f"🚌 {plano.get('desconto_caravanas', 0)}% Caravanas")
                    
                    if plano.get('desconto_bar', 0) > 0:
                        beneficios.append(f"🍺 {plano['desconto_bar']}% Bar da Torcida")
                    
                    if plano.get('inclui_camisa', False):
                        camisa_tipo = plano.get('camisa_tipo', 'Camisa')
                        beneficios.append(f"👕 {camisa_tipo} incluída")
                    
                    if plano.get('sorteio_mensal', False):
                        beneficios.append("🎲 Sorteio Mensal")
                    
                    if plano.get('grupo_exclusivo', False):
                        beneficios.append("👥 Grupo Exclusivo")
                    
                    # Exibir benefícios de forma compacta
                    for beneficio in beneficios:
                        st.markdown(f"<div style='text-align: left; margin: 5px 0; color: #eee;'>{beneficio}</div>", unsafe_allow_html=True)
                
                # Botão de seleção com estilo diferente se já selecionado
                if is_selected:
                    if st.button("✅ Plano Selecionado", key=f"plano_{plano['id']}", use_container_width=True, disabled=True):
                        pass
                else:
                    if st.button(f"🎯 Selecionar {plano['nome']}", key=f"plano_{plano['id']}", use_container_width=True, type="primary"):
                        st.session_state['plano_selecionado'] = plano['id']
                        st.rerun()
        
        # Mostrar plano selecionado com destaque
        if 'plano_selecionado' in st.session_state:
            plano_id = st.session_state['plano_selecionado']
            plano_info = next((p for p in planos if p['id'] == plano_id), None)
            
            if plano_info:
                # Determinar cor do plano selecionado
                plano_nome = plano_info['nome'].split()[-1] if ' ' in plano_info['nome'] else plano_info['nome']
                card_color = colors.get(plano_nome, '#1a1a1a')
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {card_color}20, {card_color}40);
                    border: 3px solid {card_color};
                    border-radius: 15px;
                    padding: 20px;
                    margin: 20px 0;
                    text-align: center;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                ">
                    <h3 style="color: {card_color}; margin: 0 0 15px 0; font-size: 1.8em;">
                        ✅ PLANO SELECIONADO
                    </h3>
                    <div style="font-size: 2.5em; font-weight: bold; color: {card_color}; margin: 10px 0;">
                        {plano_info['nome']}
                    </div>
                    <div style="font-size: 2em; font-weight: bold; color: {card_color}; margin: 10px 0;">
                        R$ {plano_info['valor']:.2f}
                    </div>
                    <div style="color: #fff; margin: 10px 0; font-size: 1.2em;">
                        {plano_info['periodicidade']}
                    </div>
                    <div style="color: #ddd; margin-top: 15px;">
                        Você pode alterar sua escolha a qualquer momento
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botões de ação
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    if st.button("🔄 Trocar Plano", key="trocar_plano", use_container_width=True):
                        del st.session_state['plano_selecionado']
                        st.rerun()
                
                return plano_id
        
        return None
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar planos: {e}")
        st.info("Tente recarregar a página ou entre em contato conosco.")
        return None

def show():
    """Mostrar página de cadastro público"""
    
    # Botão para voltar ao login
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("⬅️ Voltar ao Login", use_container_width=True):
            if 'page' in st.session_state:
                del st.session_state['page']
            st.rerun()
    
    # CSS personalizado para a página
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #ff0000, #cc0000);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .form-section {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ff0000;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff0000, #cc0000);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #cc0000, #990000);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header principal com logo
    st.markdown("""
    <div class="main-header">
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="app/static/logo.png" alt="UT-SOCIOS" style="width: 120px; height: 120px; margin-bottom: 15px;">
            <h1 style="margin: 0; font-size: 2.5em;">UT-SOCIOS</h1>
            <h2 style="margin: 10px 0 0 0; font-size: 1.5em;">Torne-se um Sócio da União!</h2>
            <p style="margin: 10px 0 0 0; font-size: 1.1em;">Junte-se à nossa torcida e aproveite benefícios exclusivos</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar se há comandos disponíveis
    comandos = get_comandos()
    if not comandos:
        st.error("⚠️ Sistema temporariamente indisponível. Nenhum comando cadastrado.")
        st.info("Entre em contato conosco para mais informações.")
        return
    
    # Seção de planos
    plano_selecionado_id = show_planos_cards()
    
    st.markdown("---")
    
    # Formulário de cadastro
    st.markdown("### 📝 Preencha seus Dados")
    
    with st.form("cadastro_publico_form", clear_on_submit=True):
        
        # Seção 1: Dados Pessoais
        st.markdown("#### 📋 Dados Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_completo = st.text_input(
                "Nome Completo *",
                placeholder="Digite seu nome completo"
            )
            
            cpf = st.text_input(
                "CPF *",
                placeholder="000.000.000-00",
                max_chars=14
            )
            
            data_nascimento = st.date_input(
                "Data de Nascimento *",
                min_value=date(1920, 1, 1),
                max_value=date.today(),
                value=date(1990, 1, 1)
            )
            
            email = st.text_input(
                "Email *",
                placeholder="seu@email.com"
            )
        
        with col2:
            telefone = st.text_input(
                "Telefone/WhatsApp *",
                placeholder="(00) 90000-0000",
                max_chars=15
            )
            
            # Campo de tamanho da camisa (só aparece se plano inclui camisa)
            tamanho_camisa = "M"  # Valor padrão
            
            # Verificar se há plano selecionado e se inclui camisa
            plano_inclui_camisa = False
            if 'plano_selecionado' in st.session_state:
                plano_selecionado_id = st.session_state['plano_selecionado']
                plano_info = next((p for p in get_planos() if p['id'] == plano_selecionado_id), None)
                if plano_info and plano_info.get('inclui_camisa', False):
                    plano_inclui_camisa = True
            
            if plano_inclui_camisa:
                st.info("👕 O plano selecionado inclui camisa! Escolha o tamanho:")
                tamanho_camisa = st.selectbox(
                    "Tamanho da Camisa *",
                    options=["PP", "P", "M", "G", "GG", "XG", "XXG"],
                    help="Tamanho da camisa inclusa no plano selecionado",
                    index=2  # M como padrão
                )
            else:
                # Mostrar mensagem informativa
                if 'plano_selecionado' not in st.session_state:
                    st.info("ℹ️ Selecione um plano acima para ver se inclui camisa")
                
                # Campo com valor padrão
                tamanho_camisa = st.selectbox(
                    "Tamanho da Camisa",
                    options=["PP", "P", "M", "G", "GG", "XG", "XXG"],
                    help="Para eventos e materiais do clube (opcional)",
                    index=2,  # M como padrão
                    disabled=True
                )
        
        st.markdown("---")
        
        # Seção 1.5: Foto do Sócio
        st.markdown("#### 📸 Foto do Sócio")
        foto_uploaded = create_photo_upload_widget(
            "📸 Foto do Sócio (Opcional)",
            "Faça upload de uma foto sua (JPG, PNG, GIF, BMP - máx. 5MB)"
        )
        
        st.markdown("---")
        
        # Seção 2: Comando
        st.markdown("#### 🏛️ Comando")
        
        comando_options = {c['id']: c['nome'] for c in comandos}
        comando_id = st.selectbox(
            "Escolha seu Comando *",
            options=list(comando_options.keys()),
            format_func=lambda x: comando_options[x],
            help="Comando ao qual você deseja se filiar"
        )
        
        st.markdown("---")
        
        # Seção 3: Endereço
        st.markdown("#### 📍 Endereço")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cep = st.text_input(
                "CEP",
                placeholder="00000-000",
                max_chars=9
            )
            
            endereco = st.text_input(
                "Endereço",
                placeholder="Rua/Avenida"
            )
            
            numero = st.text_input(
                "Número",
                placeholder="123"
            )
            
            complemento = st.text_input(
                "Complemento",
                placeholder="Apto, casa, etc."
            )
        
        with col2:
            bairro = st.text_input(
                "Bairro",
                placeholder="Nome do bairro"
            )
            
            cidade = st.text_input(
                "Cidade",
                placeholder="Sua cidade"
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
                help="Selecione seu estado"
            )
        
        st.markdown("---")
        
        # Seção 4: Botões
        st.markdown("#### ✅ Finalizar Cadastro")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            submit_button = st.form_submit_button(
                "🚀 Tornar-se Sócio",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            if st.form_submit_button("🔄 Limpar", use_container_width=True):
                st.rerun()
        
        # Processamento do formulário
        if submit_button:
            # Validações
            errors = []
            
            if not nome_completo.strip():
                errors.append("Nome completo é obrigatório")
            
            if not cpf.strip():
                errors.append("CPF é obrigatório")
            elif not validate_cpf(cpf):
                errors.append("CPF inválido")
            
            if not data_nascimento:
                errors.append("Data de nascimento é obrigatória")
            elif (date.today().year - data_nascimento.year) < 16 or (date.today().year - data_nascimento.year) > 100:
                errors.append("Você deve ter entre 16 e 100 anos")
            
            if not email.strip():
                errors.append("Email é obrigatório")
            elif not validate_email(email):
                errors.append("Email inválido")
            
            if not telefone.strip():
                errors.append("Telefone é obrigatório")
            elif not validate_phone(telefone):
                errors.append("Telefone inválido")
            
            # Validar tamanho da camisa apenas se plano inclui camisa
            if plano_inclui_camisa and not tamanho_camisa:
                errors.append("Tamanho da camisa é obrigatório para este plano")
            
            if not comando_id:
                errors.append("Comando é obrigatório")
            
            if cep and not validate_cep(cep):
                errors.append("CEP inválido")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Processar dados
                cpf_limpo = ''.join(filter(str.isdigit, cpf))
                telefone_limpo = ''.join(filter(str.isdigit, telefone))
                cep_limpo = ''.join(filter(str.isdigit, cep)) if cep else None
                
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
                
                # Processar foto
                foto_path = None
                if foto_uploaded:
                    with st.spinner("Salvando foto..."):
                        foto_path, error = save_socio_photo(foto_uploaded)
                        if error:
                            st.error(f"Erro ao salvar foto: {error}")
                            return
                
                # Processar plano
                plano_id_final = plano_selecionado_id if plano_selecionado_id else None
                
                # Salvar sócio
                success, message = create_socio_publico(
                    nome_completo.strip(), 
                    cpf_limpo, 
                    data_nascimento, 
                    email.strip().lower(), 
                    telefone_limpo, 
                    tamanho_camisa, 
                    comando_id, 
                    foto_path,
                    plano_id_final, 
                    endereco_data
                )
                
                if success:
                    st.success("🎉 Parabéns! Você agora é um Sócio da União!")
                    st.balloons()
                    
                    # Mostrar informações do plano se selecionado
                    if plano_id_final:
                        plano_info = next((p for p in get_planos() if p['id'] == plano_id_final), None)
                        if plano_info:
                            st.info(f"📋 **Plano selecionado**: {plano_info['nome']} - R$ {plano_info['valor']:.2f}")
                            st.info(f"📅 **Vencimento**: {format_date(date.today() + timedelta(days=365))}")
                    
                    st.markdown("---")
                    st.markdown("### 📞 Próximos Passos:")
                    st.markdown("1. **Aguardar contato** da equipe para confirmação")
                    st.markdown("2. **Efetuar pagamento** do plano escolhido")
                    st.markdown("3. **Receber materiais** e benefícios")
                    st.markdown("4. **Participar de eventos** exclusivos")
                    
                    # Limpar formulário
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # Footer informativo
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 2rem;">
        <h4>🤝 Junte-se à Nossa Família!</h4>
        <p>Seja bem-vindo à maior torcida do estado!</p>
        <p>Para dúvidas, entre em contato conosco.</p>
    </div>
    """, unsafe_allow_html=True)
