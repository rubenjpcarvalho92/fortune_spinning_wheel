from flask_restful import Resource, reqparse, marshal_with, fields
from models.funcionario import FuncionarioModel

from models import db

import logging

logger = logging.getLogger(__name__)

# Definição dos campos para serialização
resource_fields_funcionario = {
    'NIF': fields.String,
    'nomeFuncionario': fields.String,
    'passwordFuncionario': fields.String
}

# Parser para validação de entradas
funcionario_create_arg = reqparse.RequestParser()
funcionario_create_arg.add_argument("NIF", type=str, help="NIF do funcionário é obrigatório e deve ter 9 caracteres.")
funcionario_create_arg.add_argument("nomeFuncionario", type=str, help="Nome do funcionário é obrigatório.")
funcionario_create_arg.add_argument("passwordFuncionario", type=str, help="Senha do funcionário é obrigatória.")

class Funcionario(Resource):
    @marshal_with(resource_fields_funcionario)
    def get(self, NIF):
        try:
            funcionario = FuncionarioModel.query.get(NIF)
            if not funcionario:
                logger.warning(f"Funcionário com NIF {NIF} não encontrado.")
                abort(404, message=f"Funcionário com NIF {NIF} não encontrado.")
            return funcionario
        except Exception as e:
            logger.error(f"Erro ao buscar funcionário com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao buscar o funcionário.")

    @marshal_with(resource_fields_funcionario)
    def post(self):
        args = funcionario_create_arg.parse_args()
        try:
            # Verificar se o funcionário já existe
            if FuncionarioModel.query.get(args['NIF']):
                abort(409, message=f"Funcionário com NIF {args['NIF']} já está registrado.")

            funcionario = FuncionarioModel(
                NIF=args['NIF'],
                nomeFuncionario=args['nomeFuncionario'],
                passwordFuncionario=args['passwordFuncionario']
            )
            db.session.add(funcionario)
            db.session.commit()
            logger.info(f"Funcionário registrado com sucesso: {funcionario}")
            return funcionario, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao registrar funcionário: {str(e)}")
            abort(500, message="Erro interno ao registrar o funcionário.")

    @marshal_with(resource_fields_funcionario)
    def put(self, NIF):
        args = funcionario_create_arg.parse_args()
        try:
            funcionario = FuncionarioModel.query.get(NIF)
            if not funcionario:
                abort(404, message=f"Funcionário com NIF {NIF} não encontrado.")

            # Atualizar os campos
            funcionario.nomeFuncionario = args['nomeFuncionario']
            funcionario.passwordFuncionario = args['passwordFuncionario']
            db.session.commit()
            logger.info(f"Funcionário atualizado com sucesso: {funcionario}")
            return funcionario, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar funcionário com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao atualizar o funcionário.")

    def delete(self, NIF):
        try:
            funcionario = FuncionarioModel.query.get(NIF)
            if not funcionario:
                abort(404, message=f"Funcionário com NIF {NIF} não encontrado.")

            db.session.delete(funcionario)
            db.session.commit()
            logger.info(f"Funcionário com NIF {NIF} excluído com sucesso.")
            return {'message': 'Funcionário excluído com sucesso.'}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir funcionário com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao excluir o funcionário.")
