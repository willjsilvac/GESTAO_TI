#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
from src.models.user import db, Usuario
from flask import Flask
import bcrypt

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    # Buscar o usuário administrador
    admin = Usuario.query.filter_by(email='admin@empresa.com').first()
    
    if admin:
        # Atualizar a senha
        admin.set_senha('admin123')
        db.session.commit()
        print("Senha do administrador atualizada com sucesso!")
    else:
        print("Usuário administrador não encontrado!")

