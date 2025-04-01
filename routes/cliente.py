from flask_restful import Resource, reqparse, marshal_with, fields
from models.cliente import ClienteModel

from models import db

import logging

logger = logging.getLogger(__name__)

# Definição dos campos para serialização
resource_fields_cliente = {
    'NIF': fields.String,
    'nomeCliente': fields.String,
    'passwordCliente': fields.String
}

# Parser para validação de entradas
cliente_create_arg = reqparse.RequestParser()
cliente_create_arg.add_argument("NIF", type=str, help="NIF do cliente é obrigatório e deve ter 9 caracteres.")
cliente_create_arg.add_argument("nomeCliente", type=str, help="Nome do cliente é obrigatório.")
cliente_create_arg.add_argument("passwordCliente", type=str, help="Senha do cliente é obrigatória.")

class Cliente(Resource):
    @marshal_with(resource_fields_cliente)
    def get(self, NIF):
        try:
            cliente = ClienteModel.query.get(NIF)
            if not cliente:
                logger.warning(f"Cliente com NIF {NIF} não encontrado.")
                abort(404, message=f"Cliente com NIF {NIF} não encontrado.")
            return cliente
        except Exception as e:
            logger.error(f"Erro ao buscar cliente com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao buscar o cliente.")

    @marshal_with(resource_fields_cliente)
    def post(self):
        args = cliente_create_arg.parse_args()
        try:
            # Verificar se o cliente já existe
            if ClienteModel.query.get(args['NIF']):
                abort(409, message=f"Cliente com NIF {args['NIF']} já está registrado.")

            cliente = ClienteModel(
                NIF=args['NIF'],
                nomeCliente=args['nomeCliente'],
                passwordCliente=args['passwordCliente']
            )
            db.session.add(cliente)
            db.session.commit()
            logger.info(f"Cliente registrado com sucesso: {cliente}")
            return cliente, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao registrar cliente: {str(e)}")
            abort(500, message="Erro interno ao registrar o cliente.")

    @marshal_with(resource_fields_cliente)
    def put(self, NIF):
        args = cliente_create_arg.parse_args()
        try:
            cliente = ClienteModel.query.get(NIF)
            if not cliente:
                abort(404, message=f"Cliente com NIF {NIF} não encontrado.")

            # Atualizar os campos
            cliente.nomeCliente = args['nomeCliente']
            cliente.passwordCliente = args['passwordCliente']
            db.session.commit()
            logger.info(f"Cliente atualizado com sucesso: {cliente}")
            return cliente, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar cliente com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao atualizar o cliente.")

    def delete(self, NIF):
        try:
            cliente = ClienteModel.query.get(NIF)
            if not cliente:
                abort(404, message=f"Cliente com NIF {NIF} não encontrado.")

            db.session.delete(cliente)
            db.session.commit()
            logger.info(f"Cliente com NIF {NIF} excluído com sucesso.")
            return {'message': 'Cliente excluído com sucesso.'}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir cliente com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao excluir o cliente.")