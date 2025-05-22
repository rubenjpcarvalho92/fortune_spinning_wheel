# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from models import db  # Importa o SQLAlchemy inicializado
from logger_config import setup_logger  # Importa o logger configurado

# Importação das rotas
from routes.maquina import Maquina
from routes.stock import Stock
from routes.talao import Talao
from routes.admin import Admin 
from routes.premio import Premio
from routes.funcionario import Funcionario
from routes.cliente import Cliente
from routes.login import Login
from routes.setup import Setup
from routes.levantamento import Levantamento

from sqlalchemy import text
from config import SQLALCHEMY_DATABASE_URI

# Inicialização do logger
logger = setup_logger()

# Inicialização da aplicação Flask
app = Flask(__name__)
logger.info("Inicializando a aplicação Flask.")

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db.init_app(app)
logger.info("Banco de dados configurado com sucesso.")

# Configura a API
api = Api(app)
api.add_resource(Maquina, '/maquinas/', '/maquinas/<string:numeroSerie>')
api.add_resource(Stock, '/stocks/', "/stocks/<string:Maquinas_numeroSerie>")
api.add_resource(Talao, "/taloes/", "/taloes/<string:numeroSerie>")
api.add_resource(Levantamento, "/levantamentos/", "/levantamentos/<string:numeroSerie>")
api.add_resource(Login, "/logins/")
api.add_resource(Premio, "/premios/")
api.add_resource(Cliente, '/clientes/', '/clientes/<string:NIF>')
api.add_resource(Admin, "/admins/", '/admins/<string:NIF>')
api.add_resource(Funcionario, "/funcionarios/", '/funcionarios/<string:NIF>')
api.add_resource(Setup, '/setups/', '/setups/<string:Maquinas_numeroSerie>')
logger.info("Rotas registradas com sucesso.")

print(app.url_map)

# ✅ Rota pingdb DEVE estar fora do bloco if
@app.route("/pingdb")
def ping_db():
    try:
        # Usa text() para executar SQL puro
        result = db.session.execute(text("SELECT 1")).scalar()
        return {"status": "sucesso", "resultado": result}, 200
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}, 500

# Bloco principal (apenas executado localmente)
if __name__ == "__main__":
    with app.app_context():
        try:
            db.Model.metadata.create_all(bind=db.engine)
            logger.info("Tabelas criadas com sucesso no banco de dados.")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas no banco de dados: {str(e)}")

    logger.info("Flask app carregado (modo WSGI - não precisa de app.run)")
    
application = app

