from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.chamado import Chamado, HistoricoChamado
from datetime import datetime

chamado_bp = Blueprint('chamado', __name__)

@chamado_bp.route('/chamados', methods=['GET'])
def listar_chamados():
    """Lista todos os chamados"""
    try:
        status_filter = request.args.get('status')
        prioridade_filter = request.args.get('prioridade')
        tecnico_filter = request.args.get('tecnico_id')
        
        query = Chamado.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        if prioridade_filter:
            query = query.filter_by(prioridade=prioridade_filter)
        if tecnico_filter:
            query = query.filter_by(tecnico_atribuido_id=tecnico_filter)
        
        chamados = query.order_by(Chamado.data_abertura.desc()).all()
        return jsonify([chamado.to_dict() for chamado in chamados]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@chamado_bp.route('/chamados', methods=['POST'])
def criar_chamado():
    """Cria um novo chamado"""
    try:
        dados = request.get_json()
        
        chamado = Chamado(
            titulo=dados['titulo'],
            descricao=dados['descricao'],
            solicitante_id=dados['solicitante_id'],
            prioridade=dados['prioridade'],
            categoria=dados.get('categoria'),
            anexo_evidencia=dados.get('anexo_evidencia')
        )
        
        # Gerar número do chamado
        chamado.numero_chamado = chamado.gerar_numero_chamado()
        
        db.session.add(chamado)
        db.session.flush()
        
        # Criar histórico inicial
        historico = HistoricoChamado(
            chamado_id=chamado.id,
            usuario_id=dados['solicitante_id'],
            acao='Chamado criado',
            descricao='Chamado aberto pelo solicitante',
            status_novo='aberto'
        )
        db.session.add(historico)
        
        db.session.commit()
        
        return jsonify(chamado.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@chamado_bp.route('/chamados/<int:chamado_id>', methods=['GET'])
def obter_chamado(chamado_id):
    """Obtém um chamado específico"""
    try:
        chamado = Chamado.query.get_or_404(chamado_id)
        resultado = chamado.to_dict()
        resultado['historico'] = [hist.to_dict() for hist in chamado.historico]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@chamado_bp.route('/chamados/<int:chamado_id>/atribuir', methods=['PUT'])
def atribuir_chamado(chamado_id):
    """Atribui um chamado a um técnico"""
    try:
        chamado = Chamado.query.get_or_404(chamado_id)
        dados = request.get_json()
        
        status_anterior = chamado.status
        chamado.tecnico_atribuido_id = dados['tecnico_id']
        chamado.status = 'em_andamento'
        chamado.data_atribuicao = datetime.utcnow()
        
        # Criar histórico
        historico = HistoricoChamado(
            chamado_id=chamado.id,
            usuario_id=dados['usuario_atribuidor_id'],
            acao='Chamado atribuído',
            descricao=f'Chamado atribuído ao técnico ID {dados["tecnico_id"]}',
            status_anterior=status_anterior,
            status_novo='em_andamento'
        )
        db.session.add(historico)
        
        db.session.commit()
        
        return jsonify(chamado.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@chamado_bp.route('/chamados/<int:chamado_id>/resolver', methods=['PUT'])
def resolver_chamado(chamado_id):
    """Resolve um chamado"""
    try:
        chamado = Chamado.query.get_or_404(chamado_id)
        dados = request.get_json()
        
        status_anterior = chamado.status
        chamado.status = 'resolvido'
        chamado.solucao = dados['solucao']
        chamado.data_resolucao = datetime.utcnow()
        
        # Criar histórico
        historico = HistoricoChamado(
            chamado_id=chamado.id,
            usuario_id=dados['usuario_id'],
            acao='Chamado resolvido',
            descricao='Solução implementada',
            status_anterior=status_anterior,
            status_novo='resolvido'
        )
        db.session.add(historico)
        
        db.session.commit()
        
        return jsonify(chamado.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@chamado_bp.route('/chamados/<int:chamado_id>/fechar', methods=['PUT'])
def fechar_chamado(chamado_id):
    """Fecha um chamado"""
    try:
        chamado = Chamado.query.get_or_404(chamado_id)
        dados = request.get_json()
        
        status_anterior = chamado.status
        chamado.status = 'fechado'
        chamado.data_fechamento = datetime.utcnow()
        
        # Criar histórico
        historico = HistoricoChamado(
            chamado_id=chamado.id,
            usuario_id=dados['usuario_id'],
            acao='Chamado fechado',
            descricao=dados.get('observacoes', 'Chamado fechado'),
            status_anterior=status_anterior,
            status_novo='fechado'
        )
        db.session.add(historico)
        
        db.session.commit()
        
        return jsonify(chamado.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

