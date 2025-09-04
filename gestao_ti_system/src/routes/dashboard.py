from flask import Blueprint, jsonify
from src.models.user import db
from src.models.compra import Compra
from src.models.ativo import Ativo
from src.models.chamado import Chamado
from src.models.inventario import Inventario
from src.models.conta_mensal import ContaMensal
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/estatisticas', methods=['GET'])
def obter_estatisticas():
    """Obtém estatísticas gerais do sistema"""
    try:
        # Estatísticas de compras
        total_compras = Compra.query.count()
        compras_pendentes = Compra.query.filter_by(status='solicitado').count()
        compras_em_andamento = Compra.query.filter_by(status='em_andamento').count()
        
        # Estatísticas de chamados
        total_chamados = Chamado.query.count()
        chamados_abertos = Chamado.query.filter_by(status='aberto').count()
        chamados_em_andamento = Chamado.query.filter_by(status='em_andamento').count()
        chamados_criticos = Chamado.query.filter_by(prioridade='critica', status='aberto').count()
        
        # Estatísticas de ativos
        total_ativos = Ativo.query.filter_by(status='ativo').count()
        
        # Licenças vencendo nos próximos 30 dias
        data_limite = date.today() + timedelta(days=30)
        licencas_vencendo = Ativo.query.filter(
            Ativo.data_vencimento_licenca.isnot(None),
            Ativo.data_vencimento_licenca <= data_limite,
            Ativo.status == 'ativo'
        ).count()
        
        # Estatísticas de inventário
        total_itens_inventario = Inventario.query.count()
        itens_estoque_baixo = len([item for item in Inventario.query.all() if item.verificar_estoque_minimo()])
        
        # Estatísticas de contas mensais
        contas_vencidas = ContaMensal.query.filter(
            ContaMensal.data_vencimento < date.today(),
            ContaMensal.status_pagamento == 'pendente'
        ).count()
        
        contas_vencendo = ContaMensal.query.filter(
            ContaMensal.data_vencimento <= date.today() + timedelta(days=7),
            ContaMensal.data_vencimento >= date.today(),
            ContaMensal.status_pagamento == 'pendente'
        ).count()
        
        return jsonify({
            'compras': {
                'total': total_compras,
                'pendentes': compras_pendentes,
                'em_andamento': compras_em_andamento
            },
            'chamados': {
                'total': total_chamados,
                'abertos': chamados_abertos,
                'em_andamento': chamados_em_andamento,
                'criticos': chamados_criticos
            },
            'ativos': {
                'total': total_ativos,
                'licencas_vencendo': licencas_vencendo
            },
            'inventario': {
                'total_itens': total_itens_inventario,
                'estoque_baixo': itens_estoque_baixo
            },
            'contas_mensais': {
                'vencidas': contas_vencidas,
                'vencendo': contas_vencendo
            }
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@dashboard_bp.route('/dashboard/alertas', methods=['GET'])
def obter_alertas():
    """Obtém alertas importantes do sistema"""
    try:
        alertas = []
        
        # Chamados críticos abertos
        chamados_criticos = Chamado.query.filter_by(prioridade='critica', status='aberto').count()
        if chamados_criticos > 0:
            alertas.append({
                'tipo': 'critico',
                'mensagem': f'{chamados_criticos} chamado(s) crítico(s) em aberto',
                'modulo': 'chamados'
            })
        
        # Licenças vencendo
        data_limite = date.today() + timedelta(days=30)
        licencas_vencendo = Ativo.query.filter(
            Ativo.data_vencimento_licenca.isnot(None),
            Ativo.data_vencimento_licenca <= data_limite,
            Ativo.status == 'ativo'
        ).count()
        if licencas_vencendo > 0:
            alertas.append({
                'tipo': 'aviso',
                'mensagem': f'{licencas_vencendo} licença(s) vencendo nos próximos 30 dias',
                'modulo': 'ativos'
            })
        
        # Estoque baixo
        itens_estoque_baixo = len([item for item in Inventario.query.all() if item.verificar_estoque_minimo()])
        if itens_estoque_baixo > 0:
            alertas.append({
                'tipo': 'aviso',
                'mensagem': f'{itens_estoque_baixo} item(ns) com estoque abaixo do mínimo',
                'modulo': 'inventario'
            })
        
        # Contas vencidas
        contas_vencidas = ContaMensal.query.filter(
            ContaMensal.data_vencimento < date.today(),
            ContaMensal.status_pagamento == 'pendente'
        ).count()
        if contas_vencidas > 0:
            alertas.append({
                'tipo': 'critico',
                'mensagem': f'{contas_vencidas} conta(s) vencida(s)',
                'modulo': 'contas_mensais'
            })
        
        return jsonify(alertas), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

