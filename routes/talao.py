from flask_restful import Resource, reqparse, marshal_with, fields, abort
from models.talao import TalaoModel
from models.maquina import MaquinaModel
from models import db
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Campos de serialização
resource_fields_talao = {
    'numeroSerie': fields.String,
    'numeroJogadas': fields.Integer,
    'valorJogadas': fields.Integer,
    'dataImpressao': fields.String,
    'impressaoOK': fields.Boolean,
    'Maquinas_numeroSerie': fields.String
}

# Parser do POST (Criação completa)
talao_create_arg = reqparse.RequestParser()
talao_create_arg.add_argument("numeroSerie", type=str, required=True)
talao_create_arg.add_argument("numeroJogadas", type=int, required=True)
talao_create_arg.add_argument("valorJogadas", type=int, required=True)
talao_create_arg.add_argument("dataImpressao", type=str)
talao_create_arg.add_argument("impressaoOK", type=bool)
talao_create_arg.add_argument("Maquinas_numeroSerie", type=str, required=True)

# Parser do PUT (não precisa pedir novamente o numeroSerie)
talao_update_arg = reqparse.RequestParser()
talao_update_arg.add_argument("dataImpressao", type=str, required=True)
talao_update_arg.add_argument("impressaoOK", type=bool, required=True)


class Talao(Resource):
    @marshal_with(resource_fields_talao)
    def get(self, numeroSerie):
        logger.info(f"Buscando talão com número de série: {numeroSerie}")
        try:
            talao = TalaoModel.query.filter_by(numeroSerie=numeroSerie).first()
            if not talao:
                logger.warning(f"Talão com número de série {numeroSerie} não encontrado.")
                abort(404, message="Talão não encontrado.")
            return talao
        except Exception as e:
            logger.error(f"Erro ao buscar talão: {str(e)}")
            abort(500, message="Erro interno ao buscar o talão.")

    @marshal_with(resource_fields_talao)
    def post(self):

        args = talao_create_arg.parse_args()
        numeroSerie = args["numeroSerie"]

        try:
            logger.info(f"Tentando criar talão com os dados: {args}")
            if TalaoModel.query.filter_by(numeroSerie=numeroSerie).first():
                abort(409, message=f"Talão com número de série {numeroSerie} já existe.")

            maquina = MaquinaModel.query.filter_by(numeroSerie=args["Maquinas_numeroSerie"]).first()
            if not maquina:
                abort(404, message=f"Máquina com número de série {args['Maquinas_numeroSerie']} não encontrada.")

            novo_talao = TalaoModel(
                numeroSerie=numeroSerie,
                numeroJogadas=args["numeroJogadas"],
                valorJogadas=args["valorJogadas"],
                dataImpressao=args.get("dataImpressao"),
                impressaoOK=args["impressaoOK"],
                Maquinas_numeroSerie=args["Maquinas_numeroSerie"]
            )

            db.session.add(novo_talao)
            db.session.commit()
            logger.info(f"Talão criado com sucesso: {novo_talao}")
            return novo_talao, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar talão: {str(e)}")
            abort(500, message="Erro interno ao criar o talão.")

    @marshal_with(resource_fields_talao)
    def put(self, numeroSerie):
        args = talao_update_arg.parse_args()
        logger.info(f"PUT recebido com args: {args}")

        try:
            logger.info(f"Tentando atualizar talão com número de série: {numeroSerie}")
            talao = TalaoModel.query.filter_by(numeroSerie=numeroSerie).first()
            if not talao:
                abort(404, message=f"Talão com número de série {numeroSerie} não encontrado.")

            if args.get("dataImpressao"):
                talao.dataImpressao = args["dataImpressao"]
            talao.impressaoOK = args["impressaoOK"]

            db.session.commit()
            logger.info(f"Talão atualizado com sucesso: {talao}")
            return talao, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar talão: {str(e)}")
            abort(500, message="Erro interno ao atualizar o talão.")
