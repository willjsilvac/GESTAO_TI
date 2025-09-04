from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.inventario import Inventario, MovimentacaoInventario
from datetime import datetime

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario', methods=['GET'])
def listar_inventario():
    """Lista todos os itens do inventário"""
    try:
        tipo_filter = request.args.get('tipo')
        estoque_baixo = request.args.get('estoque_baixo')
        
        query = Inventario.query
        
        if tipo_filter:
            query = query.filter_by(tipo_item=tipo_filter)
        
        itens = query.order_by(Inventario.nome).all()
        
        if estoque_baixo == 'true':
            itens = [item for item in itens if item.verificar_estoque_minimo()]
        
        return jsonify([item.to_dict() for item in itens]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@inventario_bp.route('/inventario', methods=['POST'])
def criar_item_inventario():
    """Cria um novo item no inventário"""
    try:
        dados = request.get_json()
        
        item = Inventario(
            tipo_item=dados['tipo_item'],
            nome=dados['nome'],
            descricao=dados.get('descricao'),
            quantidade=dados.get('quantidade', 0),
            quantidade_minima=dados.get('quantidade_minima', 0),
            localizacao=dados.get('localizacao'),
            centro_custo_id=dados.get('centro_custo_id'),
            fornecedor_id=dados.get('fornecedor_id'),
            valor_unitario=dados.get('valor_unitario'),
            observacoes=dados.get('observacoes')
        )
        
        if dados.get('data_vencimento_licenca'):
            item.data_vencimento_licenca = datetime.strptime(dados['data_vencimento_licenca'], '%Y-%m-%d').date()
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify(item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@inventario_bp.route('/inventario/<int:item_id>', methods=['GET'])
def obter_item_inventario(item_id):
    """Obtém um item específico do inventário"""
    try:
        item = Inventario.query.get_or_404(item_id)
        resultado = item.to_dict()
        resultado['movimentacoes'] = [mov.to_dict() for mov in item.movimentacoes]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@inventario_bp.route('/inventario/<int:item_id>/movimentar', methods=['POST'])
def movimentar_inventario(item_id):
    """Registra uma movimentação no inventário"""
    try:
        item = Inventario.query.get_or_404(item_id)
        dados = request.get_json()
        
        quantidade_anterior = item.quantidade
        tipo_movimentacao = dados['tipo_movimentacao']
        quantidade_movimento = dados['quantidade']
        
        # Calcular nova quantidade
        if tipo_movimentacao == 'entrada':
            nova_quantidade = quantidade_anterior + quantidade_movimento
        elif tipo_movimentacao == 'saida':
            nova_quantidade = quantidade_anterior - quantidade_movimento
            if nova_quantidade < 0:
                return jsonify({'erro': 'Quantidade insuficiente em estoque'}), 400
        elif tipo_movimentacao == 'ajuste':
            nova_quantidade = quantidade_movimento
        else:
            return jsonify({'erro': 'Tipo de movimentação inválido'}), 400
        
        # Atualizar quantidade do item
        item.quantidade = nova_quantidade
        
        # Registrar movimentação
        movimentacao = MovimentacaoInventario(
            inventario_id=item.id,
            usuario_id=dados['usuario_id'],
            tipo_movimentacao=tipo_movimentacao,
            quantidade=quantidade_movimento,
            quantidade_anterior=quantidade_anterior,
            quantidade_nova=nova_quantidade,
            motivo=dados.get('motivo')
        )
        
        db.session.add(movimentacao)
        db.session.commit()
        
        return jsonify({
            'item': item.to_dict(),
            'movimentacao': movimentacao.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@inventario_bp.route('/inventario/<int:item_id>', methods=['PUT'])
def atualizar_item_inventario(item_id):
    """Atualiza um item do inventário"""
    try:
        item = Inventario.query.get_or_404(item_id)
        dados = request.get_json()
        
        item.tipo_item = dados.get('tipo_item', item.tipo_item)
        item.nome = dados.get('nome', item.nome)
        item.descricao = dados.get('descricao', item.descricao)
        item.quantidade_minima = dados.get('quantidade_minima', item.quantidade_minima)
        item.localizacao = dados.get('localizacao', item.localizacao)
        item.centro_custo_id = dados.get('centro_custo_id', item.centro_custo_id)
        item.fornecedor_id = dados.get('fornecedor_id', item.fornecedor_id)
        item.valor_unitario = dados.get('valor_unitario', item.valor_unitario)
        item.observacoes = dados.get('observacoes', item.observacoes)
        
        if dados.get('data_vencimento_licenca'):
            item.data_vencimento_licenca = datetime.strptime(dados['data_vencimento_licenca'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify(item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@inventario_bp.route('/inventario/estoque-baixo', methods=['GET'])
def listar_estoque_baixo():
    """Lista itens com estoque abaixo do mínimo"""
    try:
        itens = Inventario.query.all()
        itens_baixo = [item for item in itens if item.verificar_estoque_minimo()]
        
        return jsonify([item.to_dict() for item in itens_baixo]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

