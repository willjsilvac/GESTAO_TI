from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.fornecedor import Fornecedor

fornecedor_bp = Blueprint('fornecedor', __name__)

@fornecedor_bp.route('/fornecedores', methods=['GET'])
def listar_fornecedores():
    """Lista todos os fornecedores"""
    try:
        fornecedores = Fornecedor.query.filter_by(ativo=True).all()
        return jsonify([fornecedor.to_dict() for fornecedor in fornecedores]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@fornecedor_bp.route('/fornecedores', methods=['POST'])
def criar_fornecedor():
    """Cria um novo fornecedor"""
    try:
        dados = request.get_json()
        
        # Verificar se o CNPJ já existe (se fornecido)
        if dados.get('cnpj'):
            fornecedor_existente = Fornecedor.query.filter_by(cnpj=dados['cnpj']).first()
            if fornecedor_existente:
                return jsonify({'erro': 'CNPJ já cadastrado'}), 400
        
        fornecedor = Fornecedor(
            nome=dados['nome'],
            cnpj=dados.get('cnpj'),
            email=dados.get('email'),
            telefone=dados.get('telefone'),
            endereco=dados.get('endereco'),
            contato_responsavel=dados.get('contato_responsavel')
        )
        
        db.session.add(fornecedor)
        db.session.commit()
        
        return jsonify(fornecedor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@fornecedor_bp.route('/fornecedores/<int:fornecedor_id>', methods=['GET'])
def obter_fornecedor(fornecedor_id):
    """Obtém um fornecedor específico"""
    try:
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        return jsonify(fornecedor.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@fornecedor_bp.route('/fornecedores/<int:fornecedor_id>', methods=['PUT'])
def atualizar_fornecedor(fornecedor_id):
    """Atualiza um fornecedor"""
    try:
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        dados = request.get_json()
        
        fornecedor.nome = dados.get('nome', fornecedor.nome)
        fornecedor.cnpj = dados.get('cnpj', fornecedor.cnpj)
        fornecedor.email = dados.get('email', fornecedor.email)
        fornecedor.telefone = dados.get('telefone', fornecedor.telefone)
        fornecedor.endereco = dados.get('endereco', fornecedor.endereco)
        fornecedor.contato_responsavel = dados.get('contato_responsavel', fornecedor.contato_responsavel)
        fornecedor.ativo = dados.get('ativo', fornecedor.ativo)
        
        db.session.commit()
        
        return jsonify(fornecedor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@fornecedor_bp.route('/fornecedores/<int:fornecedor_id>', methods=['DELETE'])
def deletar_fornecedor(fornecedor_id):
    """Desativa um fornecedor"""
    try:
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        fornecedor.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Fornecedor desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

