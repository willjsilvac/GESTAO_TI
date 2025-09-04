from flask import Blueprint, jsonify, request
from src.models.user import Usuario, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """Lista todos os usuários ativos"""
    try:
        usuarios = Usuario.query.filter_by(ativo=True).all()
        return jsonify([usuario.to_dict() for usuario in usuarios]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    """Cria um novo usuário"""
    try:
        dados = request.get_json()
        
        # Verificar se o email já existe
        usuario_existente = Usuario.query.filter_by(email=dados['email']).first()
        if usuario_existente:
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        usuario = Usuario(
            nome=dados['nome'],
            email=dados['email'],
            perfil=dados['perfil']
        )
        usuario.set_senha(dados['senha'])
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify(usuario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    """Obtém um usuário específico"""
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    """Atualiza um usuário"""
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        dados = request.get_json()
        
        usuario.nome = dados.get('nome', usuario.nome)
        usuario.email = dados.get('email', usuario.email)
        usuario.perfil = dados.get('perfil', usuario.perfil)
        usuario.ativo = dados.get('ativo', usuario.ativo)
        
        if dados.get('senha'):
            usuario.set_senha(dados['senha'])
        
        db.session.commit()
        
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    """Desativa um usuário"""
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        usuario.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Usuário desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """Autentica um usuário"""
    try:
        dados = request.get_json()
        
        usuario = Usuario.query.filter_by(email=dados['email'], ativo=True).first()
        
        if usuario and usuario.verificar_senha(dados['senha']):
            return jsonify({
                'mensagem': 'Login realizado com sucesso',
                'usuario': usuario.to_dict()
            }), 200
        else:
            return jsonify({'erro': 'Email ou senha inválidos'}), 401
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@user_bp.route('/usuarios/tecnicos', methods=['GET'])
def listar_tecnicos():
    """Lista usuários com perfil técnico ou admin"""
    try:
        tecnicos = Usuario.query.filter(
            Usuario.perfil.in_(['tecnico', 'admin', 'superadmin']),
            Usuario.ativo == True
        ).all()
        return jsonify([tecnico.to_dict() for tecnico in tecnicos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@user_bp.route('/usuarios/perfil', methods=['PUT'])
def atualizar_perfil():
    """Atualiza o perfil do usuário logado"""
    try:
        dados = request.get_json()
        
        # Por simplicidade, vamos usar o email para identificar o usuário
        # Em um sistema real, usaríamos autenticação com token
        usuario = Usuario.query.filter_by(email=dados.get('email')).first()
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Verificar senha atual se fornecida
        if dados.get('senha_atual'):
            if not usuario.verificar_senha(dados['senha_atual']):
                return jsonify({'erro': 'Senha atual incorreta'}), 400
        
        # Atualizar dados
        if dados.get('nome'):
            usuario.nome = dados['nome']
        
        # Verificar se o novo email já existe (se diferente do atual)
        if dados.get('email') and dados['email'] != usuario.email:
            email_existente = Usuario.query.filter_by(email=dados['email']).first()
            if email_existente:
                return jsonify({'erro': 'Email já está em uso'}), 400
            usuario.email = dados['email']
        
        # Atualizar senha se fornecida
        if dados.get('nova_senha'):
            usuario.definir_senha(dados['nova_senha'])
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Perfil atualizado com sucesso',
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

