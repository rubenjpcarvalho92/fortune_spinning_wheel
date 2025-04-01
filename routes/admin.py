from flask_restful import Resource, reqparse, marshal_with, fields, abort
from models.admin import AdminModel
from models import db

import logging

logger = logging.getLogger(__name__)

# Definição dos campos para serialização
resource_fields_admin = {
    'NIF': fields.String,
    'nomeAdmin': fields.String,
    'passwordAdmin': fields.String
}

# Parser para validação de entradas
admin_create_arg = reqparse.RequestParser()
admin_create_arg.add_argument("NIF", type=str, help="NIF do admin é obrigatório e deve ter 9 caracteres.")
admin_create_arg.add_argument("nomeAdmin", type=str, help="Nome do admin é obrigatório.")
admin_create_arg.add_argument("passwordAdmin", type=str, help="Senha do admin é obrigatória.")

class Admin(Resource):
    @marshal_with(resource_fields_admin)
    def get(self, NIF):
        try:
            admin = AdminModel.query.get(NIF)
            if not admin:
                logger.warning(f"Admin com NIF {NIF} não encontrado.")
                abort(404, message=f"Admin com NIF {NIF} não encontrado.")
            return admin
        except Exception as e:
            logger.error(f"Erro ao buscar admin com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao buscar o admin.")

    @marshal_with(resource_fields_admin)
    def post(self):
        args = admin_create_arg.parse_args()
        try:
            # Validação extra do NIF
            if len(args['NIF']) != 9:
                abort(400, message="O NIF deve conter exatamente 9 caracteres.")

            # Verificar se o admin já existe
            if AdminModel.query.get(args['NIF']):
                abort(409, message=f"Admin com NIF {args['NIF']} já está registrado.")

            admin = AdminModel(
                NIF=args['NIF'],
                nomeAdmin=args['nomeAdmin'],
                passwordAdmin=args['passwordAdmin']
            )
            db.session.add(admin)
            db.session.commit()
            logger.info(f"Admin registrado com sucesso: {admin}")
            return admin, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao registrar admin: {str(e)}")
            abort(500, message="Erro interno ao registrar o admin.")

    @marshal_with(resource_fields_admin)
    def put(self, NIF):
        args = admin_create_arg.parse_args()
        try:
            admin = AdminModel.query.get(NIF)
            if not admin:
                abort(404, message=f"Admin com NIF {NIF} não encontrado.")

            # Atualizar os campos
            admin.nomeAdmin = args['nomeAdmin']
            admin.passwordAdmin = args['passwordAdmin']
            db.session.commit()
            logger.info(f"Admin atualizado com sucesso: {admin}")
            return admin, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar admin com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao atualizar o admin.")

    def delete(self, NIF):
        try:
            admin = AdminModel.query.get(NIF)
            if not admin:
                abort(404, message=f"Admin com NIF {NIF} não encontrado.")

            db.session.delete(admin)
            db.session.commit()
            logger.info(f"Admin com NIF {NIF} excluído com sucesso.")
            return {'message': 'Admin excluído com sucesso.'}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir admin com NIF {NIF}: {str(e)}")
            abort(500, message="Erro interno ao excluir o admin.")
