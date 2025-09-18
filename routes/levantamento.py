from flask_restful import Resource, reqparse, marshal_with, fields, abort
from models.levantamento import LevantamentoModel
from models.maquina import MaquinaModel
from models import db
import logging

logger = logging.getLogger(__name__)

resource_fields_levantamento = {
    'numeroSerie': fields.String,
    'data': fields.String,
    'apostadoParcial': fields.Integer,
    'taxaGanhoParcial': fields.Float,
    'atribuidoParcial': fields.Float,
    'Maquinas_numeroSerie': fields.String,
    'apostadoParcialDinheiro' : fields.Integer,
    'VD': fields.Integer,
    'PT': fields.Integer,
    'CI': fields.Integer,
    'AM': fields.Integer,
    'GM': fields.Integer,
    'VR': fields.Integer,
    'LR': fields.Integer,
    'PC': fields.Integer,
    'RX': fields.Integer,
    'AZ': fields.Integer,
    'BB': fields.Integer,
    'EE': fields.Integer,
    'ARC': fields.Integer
}

levantamento_create_arg = reqparse.RequestParser()
levantamento_create_arg.add_argument("numeroSerie", type=str, required=True)
levantamento_create_arg.add_argument("data", type=str, required=True)
levantamento_create_arg.add_argument("apostadoParcial", type=int, required=True)
levantamento_create_arg.add_argument("taxaGanhoParcial", type=float, required=True)
levantamento_create_arg.add_argument("apostadoParcialDinheiro", type=int, required=True)
levantamento_create_arg.add_argument("atribuidoParcial", type=float, required=True)
levantamento_create_arg.add_argument("Maquinas_numeroSerie", type=str, required=True)
levantamento_create_arg.add_argument("VD", type=int)
levantamento_create_arg.add_argument("PT", type=int)
levantamento_create_arg.add_argument("CI", type=int)
levantamento_create_arg.add_argument("AM", type=int)
levantamento_create_arg.add_argument("GM", type=int)
levantamento_create_arg.add_argument("VR", type=int)
levantamento_create_arg.add_argument("LR", type=int)
levantamento_create_arg.add_argument("PC", type=int)
levantamento_create_arg.add_argument("RX", type=int)
levantamento_create_arg.add_argument("AZ", type=int)
levantamento_create_arg.add_argument("BB", type=int)
levantamento_create_arg.add_argument("EE", type=int)
levantamento_create_arg.add_argument("ARC", type=int)

class Levantamento(Resource):
    @marshal_with(resource_fields_levantamento)
    def get(self, numeroSerie):
        logger.info(f"Buscando levantamento com número de série: {numeroSerie}")
        try:
            lev = LevantamentoModel.query.filter_by(numeroSerie=numeroSerie).first()
            if not lev:
                abort(404, message="Levantamento não encontrado.")
            return lev
        except Exception as e:
            logger.exception("Erro ao buscar levantamento")
            abort(500, message="Erro interno ao buscar o levantamento.")

    @marshal_with(resource_fields_levantamento)
    def post(self):
        args = levantamento_create_arg.parse_args()
        _validate_non_negative_counts(args)

        numeroSerie = args["numeroSerie"]

        try:
            logger.info(f"Tentando criar levantamento: {args}")

            # idempotência simples: se já existir, devolve 409 ou o próprio registo
            existente = LevantamentoModel.query.filter_by(numeroSerie=numeroSerie).first()
            if existente:
                abort(409, message=f"Levantamento com número de série {numeroSerie} já existe.")

            maquina = MaquinaModel.query.filter_by(numeroSerie=args["Maquinas_numeroSerie"]).first()
            if not maquina:
                abort(404, message=f"Máquina com número de série {args['Maquinas_numeroSerie']} não encontrada.")

            novo = LevantamentoModel(
                numeroSerie=numeroSerie,
                data=args["data"],
                apostadoParcial=args["apostadoParcial"],
                taxaGanhoParcial=args["taxaGanhoParcial"],
                atribuidoParcial=args["atribuidoParcial"],
                Maquinas_numeroSerie=args["Maquinas_numeroSerie"],
                apostadoParcialDinheiro=args["apostadoParcialDinheiro"],  # <<< BUG corrigido
                VD=args["VD"], PT=args["PT"], CI=args["CI"], AM=args["AM"],
                GM=args["GM"], VR=args["VR"], LR=args["LR"], PC=args["PC"],
                RX=args["RX"], AZ=args["AZ"], BB=args["BB"], EE=args["EE"], ARC=args["ARC"]
            )

            db.session.add(novo)
            db.session.commit()
            logger.info(f"Levantamento criado: {novo}")
            return novo, 201

        except Exception as e:
            db.session.rollback()
            logger.exception("Erro ao criar levantamento")
            abort(500, message="Erro interno ao criar o levantamento.")
