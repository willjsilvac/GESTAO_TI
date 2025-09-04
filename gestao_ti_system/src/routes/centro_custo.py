from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.centro_custo import CentroCusto

centro_custo_bp = Blueprint('centro_custo', __name__)

@centro_custo_bp.route('/centros-custo', methods=['GET'])
def listar_centros_custo():
    """Lista todos os centros de custo"""
    try:
        centros = CentroCusto.query.filter_by(ativo=True).all()
        return jsonify([centro.to_dict() for centro in centros]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@centro_custo_bp.route('/centros-custo', methods=['POST'])
def criar_centro_custo():
    """Cria um novo centro de custo"""
    try:
        dados = request.get_json()
        
        # Verificar se o código já existe
        centro_existente = CentroCusto.query.filter_by(codigo=dados['codigo']).first()
        if centro_existente:
            return jsonify({'erro': 'Código já existe'}), 400
        
        centro = CentroCusto(
            codigo=dados['codigo'],
            nome=dados['nome'],
            descricao=dados.get('descricao', '')
        )
        
        db.session.add(centro)
        db.session.commit()
        
        return jsonify(centro.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@centro_custo_bp.route('/centros-custo/<int:centro_id>', methods=['GET'])
def obter_centro_custo(centro_id):
    """Obtém um centro de custo específico"""
    try:
        centro = CentroCusto.query.get_or_404(centro_id)
        return jsonify(centro.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@centro_custo_bp.route('/centros-custo/<int:centro_id>', methods=['PUT'])
def atualizar_centro_custo(centro_id):
    """Atualiza um centro de custo"""
    try:
        centro = CentroCusto.query.get_or_404(centro_id)
        dados = request.get_json()
        
        centro.codigo = dados.get('codigo', centro.codigo)
        centro.nome = dados.get('nome', centro.nome)
        centro.descricao = dados.get('descricao', centro.descricao)
        centro.ativo = dados.get('ativo', centro.ativo)
        
        db.session.commit()
        
        return jsonify(centro.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@centro_custo_bp.route('/centros-custo/<int:centro_id>', methods=['DELETE'])
def deletar_centro_custo(centro_id):
    """Desativa um centro de custo"""
    try:
        centro = CentroCusto.query.get_or_404(centro_id)
        centro.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Centro de custo desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

