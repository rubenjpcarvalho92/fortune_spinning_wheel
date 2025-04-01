from flask_restful import Resource, reqparse, marshal_with, fields, abort
from models.login import LoginModel
from models.maquina import MaquinaModel

from models import db

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Campos de serialização
resource_fields_login = {
    'dataLogin': fields.String,
    'nivelAcesso': fields.String,
    'NIF': fields.Integer,
    'resultado': fields.String,
    'Maquinas_numeroSerie': fields.String
}

# Parser para criação de login
login_create_arg = reqparse.RequestParser()
login_create_arg.add_argument("dataLogin", type=str, required=True)
login_create_arg.add_argument("nivelAcesso", type=str, help="Nível de acesso inválido.", required=True)
login_create_arg.add_argument("NIF", type=int, help="NIF do usuário é obrigatório.", required=True)
login_create_arg.add_argument("resultado", type=str, help="Resultado de Login é inválido", required=True)
login_create_arg.add_argument("Maquinas_numeroSerie", type=str, help="Número de série da máquina é opcional.", required=False)

class Login(Resource):
    @marshal_with(resource_fields_login)
    def get(self, dataLogin):
        try:
            login = LoginModel.query.get(dataLogin)
            if not login:
                logger.warning(f"Login com ID {dataLogin} não encontrado.")
                abort(404, message=f"Login com ID {dataLogin} não encontrado.")
            return login
        except Exception as e:
            logger.error(f"Erro ao buscar login com ID {dataLogin}: {str(e)}")
            abort(500, message="Erro interno ao buscar o login.")

    @marshal_with(resource_fields_login)
    def post(self):
        args = login_create_arg.parse_args()
        try:
            # Validar máquina associada, se fornecida
            if args.get('Maquinas_numeroSerie'):
                maquina = MaquinaModel.query.filter_by(numeroSerie=args['Maquinas_numeroSerie']).first()
                if not maquina:
                    abort(404, message=f"Máquina com número de série {args['Maquinas_numeroSerie']} não encontrada.")

            # Criar o login
            login = LoginModel(
                dataLogin=args['dataLogin'],
                nivelAcesso=args['nivelAcesso'],
                NIF=args['NIF'],
                resultado=args['resultado'],
                Maquinas_numeroSerie=args.get('Maquinas_numeroSerie')
            )
            db.session.add(login)
            db.session.commit()
            logger.info(f"Login registrado com sucesso: {login}")
            return login, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao registrar login: {str(e)}")
            abort(500, message="Erro interno ao registrar o login.")

    @marshal_with(resource_fields_login)
    def put(self, dataLogin):
        args = login_create_arg.parse_args()
        try:
            login = LoginModel.query.get(dataLogin)
            if not login:
                abort(404, message=f"Login com ID {id} não encontrado.")

            # Validar máquina associada, se fornecida
            if args.get('Maquinas_numeroSerie'):
                maquina = MaquinaModel.query.filter_by(numeroSerie=args['Maquinas_numeroSerie']).first()
                if not maquina:
                    abort(404, message=f"Máquina com número de série {args['Maquinas_numeroSerie']} não encontrada.")

            # Atualizar campos do login
            login.dataLogin = args['dataLogin']
            login.nivelAcesso = args['nivelAcesso']
            login.NIF = args['NIF']
            login.resultado = args['resultado']
            login.Maquinas_numeroSerie = args.get('Maquinas_numeroSerie')
            db.session.commit()
            logger.info(f"Login atualizado com sucesso: {login}")
            return login, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar login com ID {dataLogin}: {str(e)}")
            abort(500, message="Erro interno ao atualizar o login.")

    def delete(self, dataLogin):
        try:
            login = LoginModel.query.get(dataLogin)
            if not login:
                abort(404, message=f"Login com ID {dataLogin} não encontrado.")

            db.session.delete(login)
            db.session.commit()
            logger.info(f"Login com ID {dataLogin} excluído com sucesso.")
            return {'message': 'Login excluído com sucesso.'}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir login com ID {dataLogin}: {str(e)}")
            abort(500, message="Erro interno ao excluir o login.")
