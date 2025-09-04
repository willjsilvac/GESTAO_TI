from src.models.user import db
from datetime import datetime

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(18), unique=True)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    contato_responsavel = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'contato_responsavel': self.contato_responsavel,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

