from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.ativo import Ativo
from datetime import datetime, date

ativo_bp = Blueprint('ativo', __name__)

@ativo_bp.route('/ativos', methods=['GET'])
def listar_ativos():
    """Lista todos os ativos"""
    try:
        tipo_filter = request.args.get('tipo')
        status_filter = request.args.get('status')
        query = Ativo.query
        
        if tipo_filter:
            query = query.filter_by(tipo_ativo=tipo_filter)
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        ativos = query.order_by(Ativo.data_aquisicao.desc()).all()
        return jsonify([ativo.to_dict() for ativo in ativos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ativo_bp.route('/ativos', methods=['POST'])
def criar_ativo():
    """Cria um novo ativo"""
    try:
        dados = request.get_json()
        
        ativo = Ativo(
            tipo_ativo=dados['tipo_ativo'],
            nome=dados['nome'],
            descricao=dados.get('descricao'),
            numero_serie=dados.get('numero_serie'),
            localizacao=dados.get('localizacao'),
            responsavel_id=dados.get('responsavel_id'),
            centro_custo_id=dados['centro_custo_id'],
            data_aquisicao=datetime.strptime(dados['data_aquisicao'], '%Y-%m-%d').date(),
            valor_aquisicao=dados.get('valor_aquisicao'),
            percentual_depreciacao=dados.get('percentual_depreciacao', 30.00)
        )
        
        if dados.get('data_vencimento_licenca'):
            ativo.data_vencimento_licenca = datetime.strptime(dados['data_vencimento_licenca'], '%Y-%m-%d').date()
        
        db.session.add(ativo)
        db.session.commit()
        
        return jsonify(ativo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@ativo_bp.route('/ativos/<int:ativo_id>', methods=['GET'])
def obter_ativo(ativo_id):
    """Obtém um ativo específico"""
    try:
        ativo = Ativo.query.get_or_404(ativo_id)
        return jsonify(ativo.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ativo_bp.route('/ativos/<int:ativo_id>', methods=['PUT'])
def atualizar_ativo(ativo_id):
    """Atualiza um ativo"""
    try:
        ativo = Ativo.query.get_or_404(ativo_id)
        dados = request.get_json()
        
        ativo.tipo_ativo = dados.get('tipo_ativo', ativo.tipo_ativo)
        ativo.nome = dados.get('nome', ativo.nome)
        ativo.descricao = dados.get('descricao', ativo.descricao)
        ativo.numero_serie = dados.get('numero_serie', ativo.numero_serie)
        ativo.localizacao = dados.get('localizacao', ativo.localizacao)
        ativo.responsavel_id = dados.get('responsavel_id', ativo.responsavel_id)
        ativo.centro_custo_id = dados.get('centro_custo_id', ativo.centro_custo_id)
        ativo.valor_aquisicao = dados.get('valor_aquisicao', ativo.valor_aquisicao)
        ativo.percentual_depreciacao = dados.get('percentual_depreciacao', ativo.percentual_depreciacao)
        ativo.status = dados.get('status', ativo.status)
        
        if dados.get('data_aquisicao'):
            ativo.data_aquisicao = datetime.strptime(dados['data_aquisicao'], '%Y-%m-%d').date()
        
        if dados.get('data_vencimento_licenca'):
            ativo.data_vencimento_licenca = datetime.strptime(dados['data_vencimento_licenca'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify(ativo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@ativo_bp.route('/ativos/licencas-vencendo', methods=['GET'])
def listar_licencas_vencendo():
    """Lista ativos com licenças vencendo nos próximos 30 dias"""
    try:
        from datetime import timedelta
        data_limite = date.today() + timedelta(days=30)
        
        ativos = Ativo.query.filter(
            Ativo.data_vencimento_licenca.isnot(None),
            Ativo.data_vencimento_licenca <= data_limite,
            Ativo.status == 'ativo'
        ).order_by(Ativo.data_vencimento_licenca).all()
        
        return jsonify([ativo.to_dict() for ativo in ativos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@ativo_bp.route('/ativos/<int:ativo_id>', methods=['DELETE'])
def deletar_ativo(ativo_id):
    """Desativa um ativo"""
    try:
        ativo = Ativo.query.get_or_404(ativo_id)
        ativo.status = 'inativo'
        db.session.commit()
        
        return jsonify({'mensagem': 'Ativo desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

