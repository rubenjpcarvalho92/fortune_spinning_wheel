from flask_restful import Resource, reqparse, marshal_with, fields, abort
from flask import request
from models.premio import PremioModel
from models.talao import TalaoModel
from models import db
import logging

logger = logging.getLogger(__name__)

# 🔹 Campos de serialização
resource_fields_premio = {
    'numeroSerie': fields.String,
    'codigoRoleta': fields.String,
    'categoriaPremio': fields.Float,
    'data': fields.String,
    'Taloes_numeroSerie': fields.String,
    'contabilizado': fields.Integer
}

# 🔹 Parser para criação e atualização
premio_create_arg = reqparse.RequestParser()
premio_create_arg.add_argument("numeroSerie", type=str, required=True)
premio_create_arg.add_argument("codigoRoleta", type=str, required=True)
premio_create_arg.add_argument("categoriaPremio", type=float, required=True)
premio_create_arg.add_argument("data", type=str, required=True)
premio_create_arg.add_argument("contabilizado", type=int, required=True)
premio_create_arg.add_argument("Taloes_numeroSerie", type=str, required=True)

# 🔹 Parser para GET/PATCH múltiplos
premio_get_arg = reqparse.RequestParser()
premio_get_arg.add_argument("numeroSerie", type=str, required=True, location="args")
# 🔹 Conversor customizado
def str_to_bool(value):
    return str(value).lower() in ("true", "1", "yes")

# 🔹 Parser corrigido
premio_get_arg.add_argument("todos", type=str_to_bool, default=False, location="args")


# ✅ Classe
class Premio(Resource):

    @marshal_with(resource_fields_premio)
    def get(self):
        args = premio_get_arg.parse_args()
        numero_serie = args["numeroSerie"]
        todos = args["todos"]

        logger.info(f"[GET] numeroSerie={numero_serie} | todos={todos}")

        try:
            query = db.session.query(PremioModel).join(TalaoModel).filter(
                TalaoModel.Maquinas_numeroSerie == numero_serie
            )

            if not todos:
                query = query.filter(PremioModel.contabilizado == 0)

            premios = query.all()

            if not premios:
                logger.warning(f"[GET] Nenhum prêmio encontrado para máquina {numero_serie}")
                abort(404, message="Nenhum prêmio encontrado.")

            return premios

        except Exception as e:
            logger.error(f"[GET] Erro inesperado: {str(e)}", exc_info=True)
            abort(500, message="Erro interno.")

    @marshal_with(resource_fields_premio)
    def post(self):
        args = premio_create_arg.parse_args()
        try:
            if PremioModel.query.filter_by(numeroSerie=args['numeroSerie']).first():
                abort(409, message="Prêmio já existe.")

            talao = TalaoModel.query.filter_by(numeroSerie=args['Taloes_numeroSerie']).first()
            if not talao:
                abort(404, message="Talão não encontrado.")

            premio = PremioModel(**args)
            db.session.add(premio)
            db.session.commit()
            return premio, 201

        except Exception as e:
            db.session.rollback()
            logger.error(f"[POST] Erro ao criar prêmio: {str(e)}", exc_info=True)
            abort(500, message="Erro interno.")

    @marshal_with(resource_fields_premio)
    def put(self, numeroSerie):
        args = premio_create_arg.parse_args()
        try:
            premio = PremioModel.query.filter_by(numeroSerie=numeroSerie).first()
            if not premio:
                abort(404, message="Prêmio não encontrado.")

            premio.codigoRoleta = args['codigoRoleta']
            premio.categoriaPremio = args['categoriaPremio']
            premio.data = args['data']
            premio.contabilizado = args['contabilizado']
            premio.Taloes_numeroSerie = args['Taloes_numeroSerie']

            db.session.commit()
            return premio, 200

        except Exception as e:
            db.session.rollback()
            logger.error(f"[PUT] Erro ao atualizar prêmio: {str(e)}", exc_info=True)
            abort(500, message="Erro interno.")

    def patch(self):
        args = premio_get_arg.parse_args()
        numero_serie = args["numeroSerie"]

        logger.info(f"[PATCH] numeroSerie={numero_serie}")

        try:
            premios = db.session.query(PremioModel).join(TalaoModel).filter(
                PremioModel.contabilizado == 0,
                PremioModel.Taloes_numeroSerie == TalaoModel.numeroSerie,
                TalaoModel.Maquinas_numeroSerie == numero_serie
            ).all()

            if not premios:
                logger.warning(f"[PATCH] Nenhum prêmio não contabilizado para máquina {numero_serie}")
                return {"message": "Nenhum prêmio não contabilizado encontrado."}, 404

            for premio in premios:
                premio.contabilizado = 1

            db.session.commit()
            logger.info(f"[PATCH] {len(premios)} prêmios atualizados.")
            return {"message": f"{len(premios)} prêmios atualizados com sucesso."}, 200

        except Exception as e:
            db.session.rollback()
            logger.error(f"[PATCH] Erro ao atualizar prêmios: {str(e)}", exc_info=True)
            abort(500, message="Erro interno ao atualizar prêmios.")
