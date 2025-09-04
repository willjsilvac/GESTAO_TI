from src.models.user import db
from datetime import datetime

class Inventario(db.Model):
    __tablename__ = 'inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_item = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    quantidade_minima = db.Column(db.Integer, default=0)
    localizacao = db.Column(db.String(255))
    centro_custo_id = db.Column(db.Integer, db.ForeignKey('centros_custo.id'))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    valor_unitario = db.Column(db.Numeric(15, 2))
    data_vencimento_licenca = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    centro_custo = db.relationship('CentroCusto', backref='inventarios')
    fornecedor = db.relationship('Fornecedor', backref='inventarios')
    movimentacoes = db.relationship('MovimentacaoInventario', backref='inventario', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Inventario {self.nome}>'

    def verificar_estoque_minimo(self):
        """Verifica se o estoque está abaixo do mínimo"""
        return self.quantidade <= self.quantidade_minima

    def to_dict(self):
        return {
            'id': self.id,
            'tipo_item': self.tipo_item,
            'nome': self.nome,
            'descricao': self.descricao,
            'quantidade': self.quantidade,
            'quantidade_minima': self.quantidade_minima,
            'localizacao': self.localizacao,
            'centro_custo_id': self.centro_custo_id,
            'fornecedor_id': self.fornecedor_id,
            'valor_unitario': float(self.valor_unitario) if self.valor_unitario else None,
            'data_vencimento_licenca': self.data_vencimento_licenca.isoformat() if self.data_vencimento_licenca else None,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'centro_custo': self.centro_custo.to_dict() if self.centro_custo else None,
            'fornecedor': self.fornecedor.to_dict() if self.fornecedor else None,
            'estoque_baixo': self.verificar_estoque_minimo()
        }

class MovimentacaoInventario(db.Model):
    __tablename__ = 'movimentacao_inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    tipo_movimentacao = db.Column(db.String(20), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_anterior = db.Column(db.Integer, nullable=False)
    quantidade_nova = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.Text)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    usuario = db.relationship('Usuario', backref='movimentacoes_inventario')

    def __repr__(self):
        return f'<MovimentacaoInventario {self.tipo_movimentacao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inventario_id': self.inventario_id,
            'usuario_id': self.usuario_id,
            'tipo_movimentacao': self.tipo_movimentacao,
            'quantidade': self.quantidade,
            'quantidade_anterior': self.quantidade_anterior,
            'quantidade_nova': self.quantidade_nova,
            'motivo': self.motivo,
            'data_movimentacao': self.data_movimentacao.isoformat() if self.data_movimentacao else None,
            'usuario': self.usuario.to_dict() if self.usuario else None
        }

