from src.models.user import db
from datetime import datetime

class Chamado(db.Model):
    __tablename__ = 'chamados'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_chamado = db.Column(db.String(20), unique=True, nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    tecnico_atribuido_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    prioridade = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='aberto')
    categoria = db.Column(db.String(50))
    anexo_evidencia = db.Column(db.String(500))
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    data_atribuicao = db.Column(db.DateTime)
    data_resolucao = db.Column(db.DateTime)
    data_fechamento = db.Column(db.DateTime)
    solucao = db.Column(db.Text)

    # Relacionamentos
    solicitante = db.relationship('Usuario', foreign_keys=[solicitante_id], backref='chamados_solicitados')
    tecnico_atribuido = db.relationship('Usuario', foreign_keys=[tecnico_atribuido_id], backref='chamados_atribuidos')
    historico = db.relationship('HistoricoChamado', backref='chamado', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Chamado {self.numero_chamado}>'

    def gerar_numero_chamado(self):
        """Gera um número único para o chamado"""
        hoje = datetime.now()
        ano = hoje.year
        # Buscar o último número do ano
        ultimo_chamado = Chamado.query.filter(
            Chamado.numero_chamado.like(f'{ano}%')
        ).order_by(Chamado.numero_chamado.desc()).first()
        
        if ultimo_chamado:
            ultimo_numero = int(ultimo_chamado.numero_chamado.split('-')[1])
            novo_numero = ultimo_numero + 1
        else:
            novo_numero = 1
        
        return f'{ano}-{novo_numero:06d}'

    def to_dict(self):
        return {
            'id': self.id,
            'numero_chamado': self.numero_chamado,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'solicitante_id': self.solicitante_id,
            'tecnico_atribuido_id': self.tecnico_atribuido_id,
            'prioridade': self.prioridade,
            'status': self.status,
            'categoria': self.categoria,
            'anexo_evidencia': self.anexo_evidencia,
            'data_abertura': self.data_abertura.isoformat() if self.data_abertura else None,
            'data_atribuicao': self.data_atribuicao.isoformat() if self.data_atribuicao else None,
            'data_resolucao': self.data_resolucao.isoformat() if self.data_resolucao else None,
            'data_fechamento': self.data_fechamento.isoformat() if self.data_fechamento else None,
            'solucao': self.solucao,
            'solicitante': self.solicitante.to_dict() if self.solicitante else None,
            'tecnico_atribuido': self.tecnico_atribuido.to_dict() if self.tecnico_atribuido else None
        }

class HistoricoChamado(db.Model):
    __tablename__ = 'historico_chamados'
    
    id = db.Column(db.Integer, primary_key=True)
    chamado_id = db.Column(db.Integer, db.ForeignKey('chamados.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    acao = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    status_anterior = db.Column(db.String(20))
    status_novo = db.Column(db.String(20))
    data_acao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    usuario = db.relationship('Usuario', backref='historico_acoes')

    def __repr__(self):
        return f'<HistoricoChamado {self.acao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'chamado_id': self.chamado_id,
            'usuario_id': self.usuario_id,
            'acao': self.acao,
            'descricao': self.descricao,
            'status_anterior': self.status_anterior,
            'status_novo': self.status_novo,
            'data_acao': self.data_acao.isoformat() if self.data_acao else None,
            'usuario': self.usuario.to_dict() if self.usuario else None
        }

