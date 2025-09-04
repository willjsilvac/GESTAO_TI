from flask import Blueprint, request, jsonify
from src.utils.email_service import email_service
import json
import os
from werkzeug.utils import secure_filename

configuracoes_bp = Blueprint('configuracoes', __name__)

# Diretório para armazenar configurações
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')

# Criar diretórios se não existirem
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

@configuracoes_bp.route('/smtp', methods=['GET'])
def obter_configuracoes_smtp():
    """Obter configurações SMTP"""
    try:
        config_file = os.path.join(CONFIG_DIR, 'smtp.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Não retornar a senha por segurança
                config['senha'] = '••••••••' if config.get('senha') else ''
                return jsonify(config)
        else:
            # Retornar configuração padrão
            return jsonify({
                'servidor': '',
                'porta': '587',
                'usuario': '',
                'senha': '',
                'ssl': True,
                'remetente_nome': 'Sistema de Gestão TI',
                'remetente_email': ''
            })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@configuracoes_bp.route('/smtp', methods=['POST'])
def salvar_configuracoes_smtp():
    """Salvar configurações SMTP"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('servidor') or not data.get('usuario'):
            return jsonify({'erro': 'Servidor e usuário são obrigatórios'}), 400
        
        config_file = os.path.join(CONFIG_DIR, 'smtp.json')
        
        # Se a senha não foi alterada (veio como ••••••••), manter a anterior
        if data.get('senha') == '••••••••':
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    existing_config = json.load(f)
                    data['senha'] = existing_config.get('senha', '')
            else:
                data['senha'] = ''
        
        # Salvar configurações
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Recarregar configurações no serviço de email
        email_service.config = email_service._load_config()
        
        return jsonify({'mensagem': 'Configurações SMTP salvas com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@configuracoes_bp.route('/logo', methods=['POST'])
def salvar_logo():
    """Salvar logo da empresa"""
    try:
        if 'logo' not in request.files:
            return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['logo']
        if file.filename == '':
            return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
        
        # Validar tipo de arquivo
        allowed_extensions = {'png', 'jpg', 'jpeg', 'svg', 'gif'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400
        
        # Validar tamanho do arquivo (2MB máximo)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 2 * 1024 * 1024:  # 2MB
            return jsonify({'erro': 'Arquivo muito grande (máx. 2MB)'}), 400
        
        # Salvar arquivo
        filename = secure_filename('logo.' + file.filename.rsplit('.', 1)[1].lower())
        file_path = os.path.join(UPLOAD_DIR, filename)
        file.save(file_path)
        
        # Salvar caminho do logo nas configurações
        config_file = os.path.join(CONFIG_DIR, 'logo.json')
        with open(config_file, 'w') as f:
            json.dump({'logo_path': filename}, f)
        
        return jsonify({'mensagem': 'Logo salvo com sucesso', 'arquivo': filename})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@configuracoes_bp.route('/logo', methods=['GET'])
def obter_logo():
    """Obter logo da empresa"""
    try:
        config_file = os.path.join(CONFIG_DIR, 'logo.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                return jsonify(config)
        else:
            return jsonify({'logo_path': None})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@configuracoes_bp.route('/smtp/test', methods=['POST'])
def testar_smtp():
    """Testar configurações SMTP"""
    try:
        data = request.get_json()
        email_teste = data.get('email')
        
        if not email_teste:
            return jsonify({'erro': 'Email de teste é obrigatório'}), 400
        
        # Testar conexão
        success, message = email_service.test_connection()
        if not success:
            return jsonify({'erro': message}), 400
        
        # Enviar email de teste
        success, message = email_service.send_notification_email(
            to_email=email_teste,
            subject="Teste de Configuração SMTP",
            message="Este é um email de teste para verificar se as configurações SMTP estão funcionando corretamente.\n\nSe você recebeu este email, a configuração está funcionando!"
        )
        
        if success:
            return jsonify({'mensagem': 'Email de teste enviado com sucesso'})
        else:
            return jsonify({'erro': message}), 500
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@configuracoes_bp.route('/smtp/status', methods=['GET'])
def status_smtp():
    """Verificar status da configuração SMTP"""
    try:
        is_configured = email_service.is_configured()
        
        if is_configured:
            success, message = email_service.test_connection()
            return jsonify({
                'configurado': True,
                'conexao_ok': success,
                'mensagem': message
            })
        else:
            return jsonify({
                'configurado': False,
                'conexao_ok': False,
                'mensagem': 'SMTP não configurado'
            })
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

