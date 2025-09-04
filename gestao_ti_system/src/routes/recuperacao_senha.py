from flask import Blueprint, request, jsonify
from src.models.user import Usuario, db
from src.utils.email_service import email_service
import secrets
import hashlib
from datetime import datetime, timedelta
import json
import os

recuperacao_bp = Blueprint('recuperacao', __name__)

# Diretório para armazenar tokens temporários
TOKENS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp', 'tokens')
os.makedirs(TOKENS_DIR, exist_ok=True)

@recuperacao_bp.route('/esqueceu-senha', methods=['POST'])
def esqueceu_senha():
    """Solicitar recuperação de senha"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'erro': 'Email é obrigatório'}), 400
        
        # Verificar se o usuário existe
        usuario = Usuario.query.filter_by(email=email, ativo=True).first()
        if not usuario:
            # Por segurança, não revelamos se o email existe ou não
            return jsonify({'mensagem': 'Se o email existir, você receberá um link de recuperação'}), 200
        
        # Gerar token único
        token = secrets.token_urlsafe(32)
        
        # Criar hash do token para armazenamento seguro
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        # Salvar token temporário (válido por 1 hora)
        token_data = {
            'usuario_id': usuario.id,
            'email': usuario.email,
            'token_hash': token_hash,
            'criado_em': datetime.now().isoformat(),
            'expira_em': (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        token_file = os.path.join(TOKENS_DIR, f'{token_hash}.json')
        with open(token_file, 'w') as f:
            json.dump(token_data, f)
        
        # Em um sistema real, aqui enviaria o email
        # Tentar enviar email se SMTP estiver configurado
        if email_service.is_configured():
            success, message = email_service.send_password_recovery_email(
                email=usuario.email,
                token=token,
                user_name=usuario.nome
            )
            if not success:
                print(f"Erro ao enviar email: {message}")
        else:
            print(f"Link de recuperação: http://18.219.145.132/redefinir-senha?token={token}")
        
        return jsonify({'mensagem': 'Se o email existir, você receberá um link de recuperação'}), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@recuperacao_bp.route('/verificar-token-recuperacao', methods=['GET'])
def verificar_token():
    """Verificar se o token de recuperação é válido"""
    try:
        token = request.args.get('token')
        
        if not token:
            return jsonify({'erro': 'Token não fornecido'}), 400
        
        # Criar hash do token
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        token_file = os.path.join(TOKENS_DIR, f'{token_hash}.json')
        
        # Verificar se o arquivo do token existe
        if not os.path.exists(token_file):
            return jsonify({'erro': 'Token inválido'}), 400
        
        # Ler dados do token
        with open(token_file, 'r') as f:
            token_data = json.load(f)
        
        # Verificar se o token não expirou
        expira_em = datetime.fromisoformat(token_data['expira_em'])
        if datetime.now() > expira_em:
            # Remover token expirado
            os.remove(token_file)
            return jsonify({'erro': 'Token expirado'}), 400
        
        return jsonify({'mensagem': 'Token válido'}), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@recuperacao_bp.route('/redefinir-senha', methods=['POST'])
def redefinir_senha():
    """Redefinir senha usando token"""
    try:
        data = request.get_json()
        token = data.get('token')
        nova_senha = data.get('nova_senha')
        
        if not token or not nova_senha:
            return jsonify({'erro': 'Token e nova senha são obrigatórios'}), 400
        
        if len(nova_senha) < 6:
            return jsonify({'erro': 'A senha deve ter pelo menos 6 caracteres'}), 400
        
        # Criar hash do token
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        token_file = os.path.join(TOKENS_DIR, f'{token_hash}.json')
        
        # Verificar se o arquivo do token existe
        if not os.path.exists(token_file):
            return jsonify({'erro': 'Token inválido'}), 400
        
        # Ler dados do token
        with open(token_file, 'r') as f:
            token_data = json.load(f)
        
        # Verificar se o token não expirou
        expira_em = datetime.fromisoformat(token_data['expira_em'])
        if datetime.now() > expira_em:
            # Remover token expirado
            os.remove(token_file)
            return jsonify({'erro': 'Token expirado'}), 400
        
        # Buscar usuário
        usuario = Usuario.query.get(token_data['usuario_id'])
        if not usuario or not usuario.ativo:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Atualizar senha
        usuario.definir_senha(nova_senha)
        db.session.commit()
        
        # Remover token usado
        os.remove(token_file)
        
        return jsonify({'mensagem': 'Senha redefinida com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

def limpar_tokens_expirados():
    """Função utilitária para limpar tokens expirados"""
    try:
        for filename in os.listdir(TOKENS_DIR):
            if filename.endswith('.json'):
                token_file = os.path.join(TOKENS_DIR, filename)
                try:
                    with open(token_file, 'r') as f:
                        token_data = json.load(f)
                    
                    expira_em = datetime.fromisoformat(token_data['expira_em'])
                    if datetime.now() > expira_em:
                        os.remove(token_file)
                except:
                    # Se houver erro ao ler o arquivo, remove ele
                    os.remove(token_file)
    except:
        pass

