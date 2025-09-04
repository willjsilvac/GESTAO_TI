from flask import Blueprint, request, jsonify, current_app, send_from_directory
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_arquivo():
    """Faz upload de um arquivo"""
    try:
        if 'arquivo' not in request.files:
            return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
        
        arquivo = request.files['arquivo']
        
        if arquivo.filename == '':
            return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
        
        if arquivo and allowed_file(arquivo.filename):
            # Gerar nome único para o arquivo
            filename = secure_filename(arquivo.filename)
            nome_unico = f"{uuid.uuid4()}_{filename}"
            
            # Salvar arquivo
            caminho_arquivo = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_unico)
            arquivo.save(caminho_arquivo)
            
            return jsonify({
                'mensagem': 'Arquivo enviado com sucesso',
                'nome_arquivo': nome_unico,
                'nome_original': filename,
                'caminho': caminho_arquivo
            }), 200
        else:
            return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@upload_bp.route('/uploads/<filename>')
def download_arquivo(filename):
    """Baixa um arquivo enviado"""
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'erro': str(e)}), 404

@upload_bp.route('/uploads/<filename>/info')
def info_arquivo(filename):
    """Obtém informações sobre um arquivo"""
    try:
        caminho_arquivo = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(caminho_arquivo):
            return jsonify({'erro': 'Arquivo não encontrado'}), 404
        
        stat = os.stat(caminho_arquivo)
        
        return jsonify({
            'nome_arquivo': filename,
            'tamanho': stat.st_size,
            'data_criacao': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'data_modificacao': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

