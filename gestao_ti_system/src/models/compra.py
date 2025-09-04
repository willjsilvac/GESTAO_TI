from src.models.user import db
from datetime import datetime

class Compra(db.Model):
    __tablename__ = 'compras'
    
    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    centro_custo_id = db.Column(db.Integer, db.ForeignKey('centros_custo.id'))
    usuario_solicitante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    numero_pedido = db.Column(db.String(100), unique=True)
    descricao = db.Column(db.Text, nullable=False)
    valor_total = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='solicitado')
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_aquisicao = db.Column(db.Date)
    anexo_pedido = db.Column(db.String(500))
    anexo_nota_fiscal = db.Column(db.String(500))
    anexo_boleto = db.Column(db.String(500))
    observacoes = db.Column(db.Text)

    # Relacionamentos
    fornecedor = db.relationship('Fornecedor', backref='compras')
    centro_custo = db.relationship('CentroCusto', backref='compras')
    usuario_solicitante = db.relationship('Usuario', backref='compras_solicitadas')
    produtos = db.relationship('ProdutoAdquirido', backref='compra', cascade='all, delete-orphan')
    rateios = db.relationship('RateioCompra', backref='compra', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Compra {self.numero_pedido}>'

    def to_dict(self):
        return {
            'id': self.id,
            'fornecedor_id': self.fornecedor_id,
            'centro_custo_id': self.centro_custo_id,
            'usuario_solicitante_id': self.usuario_solicitante_id,
            'numero_pedido': self.numero_pedido,
            'descricao': self.descricao,
            'valor_total': float(self.valor_total) if self.valor_total else None,
            'status': self.status,
            'data_solicitacao': self.data_solicitacao.isoformat() if self.data_solicitacao else None,
            'data_aquisicao': self.data_aquisicao.isoformat() if self.data_aquisicao else None,
            'anexo_pedido': self.anexo_pedido,
            'anexo_nota_fiscal': self.anexo_nota_fiscal,
            'anexo_boleto': self.anexo_boleto,
            'observacoes': self.observacoes,
            'fornecedor': self.fornecedor.to_dict() if self.fornecedor else None,
            'centro_custo': self.centro_custo.to_dict() if self.centro_custo else None,
            'usuario_solicitante': self.usuario_solicitante.to_dict() if self.usuario_solicitante else None
        }

class ProdutoAdquirido(db.Model):
    __tablename__ = 'produtos_adquiridos'
    
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'))
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    valor_unitario = db.Column(db.Numeric(15, 2), nullable=False)
    valor_total = db.Column(db.Numeric(15, 2), nullable=False)

    def __repr__(self):
        return f'<ProdutoAdquirido {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'compra_id': self.compra_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'quantidade': self.quantidade,
            'valor_unitario': float(self.valor_unitario) if self.valor_unitario else None,
            'valor_total': float(self.valor_total) if self.valor_total else None
        }

class RateioCompra(db.Model):
    __tablename__ = 'rateio_compras'
    
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'))
    centro_custo_id = db.Column(db.Integer, db.ForeignKey('centros_custo.id'))
    percentual = db.Column(db.Numeric(5, 2), nullable=False)
    valor = db.Column(db.Numeric(15, 2), nullable=False)

    # Relacionamentos
    centro_custo = db.relationship('CentroCusto', backref='rateios')

    def __repr__(self):
        return f'<RateioCompra {self.percentual}%>'

    def to_dict(self):
        return {
            'id': self.id,
            'compra_id': self.compra_id,
            'centro_custo_id': self.centro_custo_id,
            'percentual': float(self.percentual) if self.percentual else None,
            'valor': float(self.valor) if self.valor else None,
            'centro_custo': self.centro_custo.to_dict() if self.centro_custo else None
        }

