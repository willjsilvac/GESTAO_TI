from src.models.user import db
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class Ativo(db.Model):
    __tablename__ = 'ativos'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_ativo = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    numero_serie = db.Column(db.String(100))
    localizacao = db.Column(db.String(255))
    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    centro_custo_id = db.Column(db.Integer, db.ForeignKey('centros_custo.id'))
    data_aquisicao = db.Column(db.Date, nullable=False)
    valor_aquisicao = db.Column(db.Numeric(15, 2))
    valor_atual = db.Column(db.Numeric(15, 2))
    percentual_depreciacao = db.Column(db.Numeric(5, 2), default=30.00)
    data_vencimento_licenca = db.Column(db.Date)
    status = db.Column(db.String(20), default='ativo')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    responsavel = db.relationship('Usuario', backref='ativos_responsaveis')
    centro_custo = db.relationship('CentroCusto', backref='ativos')

    def __repr__(self):
        return f'<Ativo {self.nome}>'

    def calcular_depreciacao(self):
        """Calcula a depreciação automática do ativo"""
        if not self.valor_aquisicao or not self.data_aquisicao:
            return self.valor_aquisicao or 0
        
        hoje = date.today()
        anos_decorridos = relativedelta(hoje, self.data_aquisicao).years
        
        if anos_decorridos <= 0:
            return float(self.valor_aquisicao)
        
        valor_depreciado = float(self.valor_aquisicao) * (float(self.percentual_depreciacao) / 100) * anos_decorridos
        
        if valor_depreciado > float(self.valor_aquisicao):
            valor_depreciado = float(self.valor_aquisicao)
        
        return float(self.valor_aquisicao) - valor_depreciado

    def to_dict(self):
        return {
            'id': self.id,
            'tipo_ativo': self.tipo_ativo,
            'nome': self.nome,
            'descricao': self.descricao,
            'numero_serie': self.numero_serie,
            'localizacao': self.localizacao,
            'responsavel_id': self.responsavel_id,
            'centro_custo_id': self.centro_custo_id,
            'data_aquisicao': self.data_aquisicao.isoformat() if self.data_aquisicao else None,
            'valor_aquisicao': float(self.valor_aquisicao) if self.valor_aquisicao else None,
            'valor_atual': self.calcular_depreciacao(),
            'percentual_depreciacao': float(self.percentual_depreciacao) if self.percentual_depreciacao else None,
            'data_vencimento_licenca': self.data_vencimento_licenca.isoformat() if self.data_vencimento_licenca else None,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'responsavel': self.responsavel.to_dict() if self.responsavel else None,
            'centro_custo': self.centro_custo.to_dict() if self.centro_custo else None
        }

