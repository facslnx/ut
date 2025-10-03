"""
Utilitário para gerenciar fotos dos sócios
"""

import os
import uuid
import streamlit as st
from PIL import Image
import io

# Configurações
UPLOAD_DIR = "uploads/socios"
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DIMENSIONS = (800, 800)  # Máximo 800x800 pixels

def ensure_upload_dir():
    """Garantir que o diretório de upload existe"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

def is_allowed_file(filename):
    """Verificar se o arquivo tem extensão permitida"""
    if not filename:
        return False
    ext = os.path.splitext(filename.lower())[1]
    return ext in ALLOWED_EXTENSIONS

def validate_image(image_bytes):
    """Validar e redimensionar imagem"""
    try:
        # Abrir imagem
        image = Image.open(io.BytesIO(image_bytes))
        
        # Verificar formato
        if image.format not in ['JPEG', 'PNG', 'GIF', 'BMP']:
            return None, "Formato de imagem não suportado"
        
        # Redimensionar se necessário
        if image.size[0] > MAX_DIMENSIONS[0] or image.size[1] > MAX_DIMENSIONS[1]:
            image.thumbnail(MAX_DIMENSIONS, Image.Resampling.LANCZOS)
        
        # Converter para RGB se necessário (para JPEG)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Salvar em bytes
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        return output.getvalue(), None
        
    except Exception as e:
        return None, f"Erro ao processar imagem: {str(e)}"

def save_socio_photo(uploaded_file, socio_id=None):
    """Salvar foto do sócio"""
    try:
        # Garantir que o diretório existe
        ensure_upload_dir()
        
        # Validar arquivo
        if not is_allowed_file(uploaded_file.name):
            return None, "Tipo de arquivo não permitido. Use JPG, PNG, GIF ou BMP."
        
        # Verificar tamanho
        if uploaded_file.size > MAX_FILE_SIZE:
            return None, f"Arquivo muito grande. Máximo permitido: {MAX_FILE_SIZE // (1024*1024)}MB"
        
        # Ler bytes do arquivo
        file_bytes = uploaded_file.read()
        
        # Validar e processar imagem
        processed_image, error = validate_image(file_bytes)
        if error:
            return None, error
        
        # Gerar nome único para o arquivo
        if socio_id:
            filename = f"socio_{socio_id}_{uuid.uuid4().hex[:8]}.jpg"
        else:
            filename = f"socio_{uuid.uuid4().hex[:12]}.jpg"
        
        # Caminho completo
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Salvar arquivo
        with open(file_path, 'wb') as f:
            f.write(processed_image)
        
        return file_path, None
        
    except Exception as e:
        return None, f"Erro ao salvar foto: {str(e)}"

def delete_socio_photo(photo_path):
    """Deletar foto do sócio"""
    try:
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
            return True
        return False
    except Exception as e:
        print(f"Erro ao deletar foto {photo_path}: {e}")
        return False

def get_photo_url(photo_path):
    """Obter URL da foto para exibição"""
    if not photo_path or not os.path.exists(photo_path):
        return None
    
    # Para Streamlit, usar caminho relativo
    return photo_path.replace('\\', '/')

def show_socio_photo(photo_path, width=150, height=150):
    """Exibir foto do sócio no Streamlit"""
    if not photo_path or not os.path.exists(photo_path):
        # Mostrar placeholder
        st.markdown(f"""
        <div style="width: {width}px; height: {height}px; background-color: #f0f0f0; 
                    border: 2px dashed #ccc; display: flex; align-items: center; 
                    justify-content: center; border-radius: 8px;">
            <span style="color: #666; font-size: 12px;">Sem foto</span>
        </div>
        """, unsafe_allow_html=True)
        return
    
    try:
        # Carregar e exibir imagem
        image = Image.open(photo_path)
        st.image(image, width=width, caption="Foto do Sócio")
    except Exception as e:
        st.error(f"Erro ao carregar foto: {e}")

def create_photo_upload_widget(label="📸 Foto do Sócio", help_text="Faça upload de uma foto (JPG, PNG, GIF, BMP - máx. 5MB)"):
    """Criar widget de upload de foto"""
    uploaded_file = st.file_uploader(
        label,
        type=['jpg', 'jpeg', 'png', 'gif', 'bmp'],
        help=help_text,
        accept_multiple_files=False
    )
    
    if uploaded_file:
        # Mostrar preview
        st.image(uploaded_file, width=200, caption="Preview da foto")
        
        # Informações do arquivo
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.info(f"📁 Arquivo: {uploaded_file.name} ({file_size_mb:.2f} MB)")
    
    return uploaded_file
