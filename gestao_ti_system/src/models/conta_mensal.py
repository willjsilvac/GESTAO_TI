from src.models.user import db
from datetime import datetime

class ContaMensal(db.Model):
    __tablename__ = 'contas_mensais'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_conta = db.Column(db.String(100), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    centro_custo_id = db.Column(db.Integer, db.ForeignKey('centros_custo.id'))
    valor = db.Column(db.Numeric(15, 2), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    status_pagamento = db.Column(db.String(20), nullable=False, default='pendente')
    recorrencia = db.Column(db.String(20))
    data_contratacao = db.Column(db.Date)
    descricao = db.Column(db.Text)
    anexo_contrato = db.Column(db.String(500))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_pagamento = db.Column(db.DateTime)

    # Relacionamentos
    fornecedor = db.relationship('Fornecedor', backref='contas_mensais')
    centro_custo = db.relationship('CentroCusto', backref='contas_mensais')

    def __repr__(self):
        return f'<ContaMensal {self.tipo_conta}>'

    def verificar_vencimento(self):
        """Verifica se a conta está vencida"""
        from datetime import date
        return self.data_vencimento < date.today() and self.status_pagamento == 'pendente'

    def to_dict(self):
        return {
            'id': self.id,
            'tipo_conta': self.tipo_conta,
            'fornecedor_id': self.fornecedor_id,
            'centro_custo_id': self.centro_custo_id,
            'valor': float(self.valor) if self.valor else None,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'status_pagamento': self.status_pagamento,
            'recorrencia': self.recorrencia,
            'data_contratacao': self.data_contratacao.isoformat() if self.data_contratacao else None,
            'descricao': self.descricao,
            'anexo_contrato': self.anexo_contrato,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'fornecedor': self.fornecedor.to_dict() if self.fornecedor else None,
            'centro_custo': self.centro_custo.to_dict() if self.centro_custo else None,
            'vencida': self.verificar_vencimento()
        }

