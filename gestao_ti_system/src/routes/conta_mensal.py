from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.conta_mensal import ContaMensal
from datetime import datetime, date

conta_mensal_bp = Blueprint('conta_mensal', __name__)

@conta_mensal_bp.route('/contas-mensais', methods=['GET'])
def listar_contas_mensais():
    """Lista todas as contas mensais"""
    try:
        status_filter = request.args.get('status')
        mes_filter = request.args.get('mes')
        ano_filter = request.args.get('ano')
        
        query = ContaMensal.query
        
        if status_filter:
            query = query.filter_by(status_pagamento=status_filter)
        
        if mes_filter and ano_filter:
            query = query.filter(
                db.extract('month', ContaMensal.data_vencimento) == int(mes_filter),
                db.extract('year', ContaMensal.data_vencimento) == int(ano_filter)
            )
        
        contas = query.order_by(ContaMensal.data_vencimento).all()
        return jsonify([conta.to_dict() for conta in contas]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@conta_mensal_bp.route('/contas-mensais', methods=['POST'])
def criar_conta_mensal():
    """Cria uma nova conta mensal"""
    try:
        dados = request.get_json()
        
        conta = ContaMensal(
            tipo_conta=dados['tipo_conta'],
            fornecedor_id=dados.get('fornecedor_id'),
            centro_custo_id=dados['centro_custo_id'],
            valor=dados['valor'],
            data_vencimento=datetime.strptime(dados['data_vencimento'], '%Y-%m-%d').date(),
            recorrencia=dados.get('recorrencia'),
            descricao=dados.get('descricao'),
            anexo_contrato=dados.get('anexo_contrato')
        )
        
        if dados.get('data_contratacao'):
            conta.data_contratacao = datetime.strptime(dados['data_contratacao'], '%Y-%m-%d').date()
        
        db.session.add(conta)
        db.session.commit()
        
        return jsonify(conta.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@conta_mensal_bp.route('/contas-mensais/<int:conta_id>', methods=['GET'])
def obter_conta_mensal(conta_id):
    """Obtém uma conta mensal específica"""
    try:
        conta = ContaMensal.query.get_or_404(conta_id)
        return jsonify(conta.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@conta_mensal_bp.route('/contas-mensais/<int:conta_id>', methods=['PUT'])
def atualizar_conta_mensal(conta_id):
    """Atualiza uma conta mensal"""
    try:
        conta = ContaMensal.query.get_or_404(conta_id)
        dados = request.get_json()
        
        conta.tipo_conta = dados.get('tipo_conta', conta.tipo_conta)
        conta.fornecedor_id = dados.get('fornecedor_id', conta.fornecedor_id)
        conta.centro_custo_id = dados.get('centro_custo_id', conta.centro_custo_id)
        conta.valor = dados.get('valor', conta.valor)
        conta.status_pagamento = dados.get('status_pagamento', conta.status_pagamento)
        conta.recorrencia = dados.get('recorrencia', conta.recorrencia)
        conta.descricao = dados.get('descricao', conta.descricao)
        conta.anexo_contrato = dados.get('anexo_contrato', conta.anexo_contrato)
        
        if dados.get('data_vencimento'):
            conta.data_vencimento = datetime.strptime(dados['data_vencimento'], '%Y-%m-%d').date()
        
        if dados.get('data_contratacao'):
            conta.data_contratacao = datetime.strptime(dados['data_contratacao'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify(conta.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@conta_mensal_bp.route('/contas-mensais/<int:conta_id>/pagar', methods=['PUT'])
def pagar_conta_mensal(conta_id):
    """Marca uma conta como paga"""
    try:
        conta = ContaMensal.query.get_or_404(conta_id)
        
        conta.status_pagamento = 'pago'
        conta.data_pagamento = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(conta.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@conta_mensal_bp.route('/contas-mensais/vencidas', methods=['GET'])
def listar_contas_vencidas():
    """Lista contas vencidas"""
    try:
        contas = ContaMensal.query.filter(
            ContaMensal.data_vencimento < date.today(),
            ContaMensal.status_pagamento == 'pendente'
        ).order_by(ContaMensal.data_vencimento).all()
        
        return jsonify([conta.to_dict() for conta in contas]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@conta_mensal_bp.route('/contas-mensais/vencendo', methods=['GET'])
def listar_contas_vencendo():
    """Lista contas vencendo nos próximos 7 dias"""
    try:
        from datetime import timedelta
        data_limite = date.today() + timedelta(days=7)
        
        contas = ContaMensal.query.filter(
            ContaMensal.data_vencimento <= data_limite,
            ContaMensal.data_vencimento >= date.today(),
            ContaMensal.status_pagamento == 'pendente'
        ).order_by(ContaMensal.data_vencimento).all()
        
        return jsonify([conta.to_dict() for conta in contas]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

