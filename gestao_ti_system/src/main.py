import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.config import Config
from src.models.user import db

# Importar todos os modelos
from src.models.user import Usuario
from src.models.centro_custo import CentroCusto
from src.models.fornecedor import Fornecedor
from src.models.compra import Compra, ProdutoAdquirido, RateioCompra
from src.models.ativo import Ativo
from src.models.chamado import Chamado, HistoricoChamado
from src.models.inventario import Inventario, MovimentacaoInventario
from src.models.conta_mensal import ContaMensal

# Importar blueprints
from src.routes.user import user_bp
from src.routes.centro_custo import centro_custo_bp
from src.routes.fornecedor import fornecedor_bp
from src.routes.compra import compra_bp
from src.routes.ativo import ativo_bp
from src.routes.chamado import chamado_bp
from src.routes.inventario import inventario_bp
from src.routes.conta_mensal import conta_mensal_bp
from src.routes.upload import upload_bp
from src.routes.dashboard import dashboard_bp
from src.routes.configuracoes import configuracoes_bp
from src.routes.recuperacao_senha import recuperacao_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config.from_object(Config)

# Habilitar CORS para todas as rotas
CORS(app)

# Criar diretório de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(centro_custo_bp, url_prefix='/api')
app.register_blueprint(fornecedor_bp, url_prefix='/api')
app.register_blueprint(compra_bp, url_prefix='/api')
app.register_blueprint(ativo_bp, url_prefix='/api')
app.register_blueprint(chamado_bp, url_prefix='/api')
app.register_blueprint(inventario_bp, url_prefix='/api')
app.register_blueprint(conta_mensal_bp, url_prefix='/api')
app.register_blueprint(upload_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')
app.register_blueprint(configuracoes_bp, url_prefix='/api/configuracoes')
app.register_blueprint(recuperacao_bp, url_prefix='/api')

# Configuração do banco de dados PostgreSQL
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
