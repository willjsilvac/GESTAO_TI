from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.compra import Compra, ProdutoAdquirido, RateioCompra
from datetime import datetime

compra_bp = Blueprint('compra', __name__)

@compra_bp.route('/compras', methods=['GET'])
def listar_compras():
    """Lista todas as compras"""
    try:
        status_filter = request.args.get('status')
        query = Compra.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        compras = query.order_by(Compra.data_solicitacao.desc()).all()
        return jsonify([compra.to_dict() for compra in compras]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@compra_bp.route('/compras', methods=['POST'])
def criar_compra():
    """Cria uma nova compra"""
    try:
        dados = request.get_json()
        
        # Gerar número do pedido automaticamente
        hoje = datetime.now()
        ano = hoje.year
        ultimo_pedido = Compra.query.filter(
            Compra.numero_pedido.like(f'PED{ano}%')
        ).order_by(Compra.numero_pedido.desc()).first()
        
        if ultimo_pedido:
            ultimo_numero = int(ultimo_pedido.numero_pedido.replace(f'PED{ano}', ''))
            novo_numero = ultimo_numero + 1
        else:
            novo_numero = 1
        
        numero_pedido = f'PED{ano}{novo_numero:06d}'
        
        compra = Compra(
            fornecedor_id=dados['fornecedor_id'],
            centro_custo_id=dados['centro_custo_id'],
            usuario_solicitante_id=dados['usuario_solicitante_id'],
            numero_pedido=numero_pedido,
            descricao=dados['descricao'],
            valor_total=dados['valor_total'],
            observacoes=dados.get('observacoes')
        )
        
        db.session.add(compra)
        db.session.flush()  # Para obter o ID da compra
        
        # Adicionar produtos adquiridos
        if 'produtos' in dados:
            for produto_data in dados['produtos']:
                produto = ProdutoAdquirido(
                    compra_id=compra.id,
                    nome=produto_data['nome'],
                    descricao=produto_data.get('descricao'),
                    quantidade=produto_data['quantidade'],
                    valor_unitario=produto_data['valor_unitario'],
                    valor_total=produto_data['valor_total']
                )
                db.session.add(produto)
        
        # Adicionar rateios
        if 'rateios' in dados:
            for rateio_data in dados['rateios']:
                rateio = RateioCompra(
                    compra_id=compra.id,
                    centro_custo_id=rateio_data['centro_custo_id'],
                    percentual=rateio_data['percentual'],
                    valor=rateio_data['valor']
                )
                db.session.add(rateio)
        
        db.session.commit()
        
        return jsonify(compra.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@compra_bp.route('/compras/<int:compra_id>', methods=['GET'])
def obter_compra(compra_id):
    """Obtém uma compra específica"""
    try:
        compra = Compra.query.get_or_404(compra_id)
        resultado = compra.to_dict()
        resultado['produtos'] = [produto.to_dict() for produto in compra.produtos]
        resultado['rateios'] = [rateio.to_dict() for rateio in compra.rateios]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@compra_bp.route('/compras/<int:compra_id>', methods=['PUT'])
def atualizar_compra(compra_id):
    """Atualiza uma compra"""
    try:
        compra = Compra.query.get_or_404(compra_id)
        dados = request.get_json()
        
        compra.fornecedor_id = dados.get('fornecedor_id', compra.fornecedor_id)
        compra.centro_custo_id = dados.get('centro_custo_id', compra.centro_custo_id)
        compra.descricao = dados.get('descricao', compra.descricao)
        compra.valor_total = dados.get('valor_total', compra.valor_total)
        compra.status = dados.get('status', compra.status)
        compra.observacoes = dados.get('observacoes', compra.observacoes)
        
        if dados.get('data_aquisicao'):
            compra.data_aquisicao = datetime.strptime(dados['data_aquisicao'], '%Y-%m-%d').date()
        
        # Atualizar anexos
        compra.anexo_pedido = dados.get('anexo_pedido', compra.anexo_pedido)
        compra.anexo_nota_fiscal = dados.get('anexo_nota_fiscal', compra.anexo_nota_fiscal)
        compra.anexo_boleto = dados.get('anexo_boleto', compra.anexo_boleto)
        
        db.session.commit()
        
        return jsonify(compra.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@compra_bp.route('/compras/<int:compra_id>/status', methods=['PUT'])
def atualizar_status_compra(compra_id):
    """Atualiza apenas o status de uma compra"""
    try:
        compra = Compra.query.get_or_404(compra_id)
        dados = request.get_json()
        
        compra.status = dados['status']
        
        if dados['status'] == 'entregue' and not compra.data_aquisicao:
            compra.data_aquisicao = datetime.now().date()
        
        db.session.commit()
        
        return jsonify(compra.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

