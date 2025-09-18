from flask import jsonify, make_response
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
    'apostadoParcialDinheiro': fields.Integer,
    'VD': fields.Integer, 'PT': fields.Integer, 'CI': fields.Integer, 'AM': fields.Integer,
    'GM': fields.Integer, 'VR': fields.Integer, 'LR': fields.Integer, 'PC': fields.Integer,
    'RX': fields.Integer, 'AZ': fields.Integer, 'BB': fields.Integer, 'EE': fields.Integer, 'ARC': fields.Integer
}

def abort_json(status, message):
    resp = make_response(jsonify({"error": message}), status)
    resp.headers["Content-Type"] = "application/json"
    abort(resp)

def _validate_non_negative_counts(args):
    bad = {k: args.get(k, 0) for k in ["VD","PT","CI","AM","GM","VR","LR","PC","RX","AZ","BB","EE","ARC"]
           if args.get(k) is not None and args.get(k) < 0}
    if bad:
        abort_json(400, f"Quantidades negativas: {bad}")

levantamento_create_arg = reqparse.RequestParser()
for name, typ, req in [
    ("numeroSerie", str, True),
    ("data", str, True),  # a tua coluna é VARCHAR -> guarda string
    ("apostadoParcial", int, True),
    ("taxaGanhoParcial", float, True),
    ("atribuidoParcial", float, True),
    ("apostadoParcialDinheiro", int, True),  # NOT NULL na BD
    ("Maquinas_numeroSerie", str, True),
]:
    levantamento_create_arg.add_argument(name, type=typ, required=req)

# defaults 0 para não mandares None
for p in ["VD","PT","CI","AM","GM","VR","LR","PC","RX","AZ","BB","EE","ARC"]:
    levantamento_create_arg.add_argument(p, type=int, required=False, default=0)

class Levantamento(Resource):

    @marshal_with(resource_fields_levantamento)
    def get(self, numeroSerie):
        logger.info(f"Buscando levantamento {numeroSerie}")
        try:
            lev = LevantamentoModel.query.filter_by(numeroSerie=numeroSerie).first()
            if not lev:
                abort_json(404, "Levantamento não encontrado.")
            return lev, 200
        except Exception:
            logger.exception("Erro ao buscar levantamento")
            abort_json(500, "Erro interno ao buscar o levantamento.")

    # Não usar marshal_with aqui porque em erro devolvemos {"error":...}
    def post(self):
        args = levantamento_create_arg.parse_args()
        _validate_non_negative_counts(args)

        numeroSerie = args["numeroSerie"]
        try:
            # idempotência
            if LevantamentoModel.query.filter_by(numeroSerie=numeroSerie).first():
                abort_json(409, f"Levantamento {numeroSerie} já existe.")

            # FK: a máquina tem de existir
            maquina = MaquinaModel.query.filter_by(numeroSerie=args["Maquinas_numeroSerie"]).first()
            if not maquina:
                abort_json(404, f"Máquina {args['Maquinas_numeroSerie']} não encontrada.")

            novo = LevantamentoModel(
                numeroSerie=numeroSerie,
                data=args["data"],  # string
                apostadoParcial=args["apostadoParcial"],
                taxaGanhoParcial=args["taxaGanhoParcial"],
                atribuidoParcial=args["atribuidoParcial"],
                Maquinas_numeroSerie=args["Maquinas_numeroSerie"],
                apostadoParcialDinheiro=args["apostadoParcialDinheiro"],
                VD=args["VD"], PT=args["PT"], CI=args["CI"], AM=args["AM"],
                GM=args["GM"], VR=args["VR"], LR=args["LR"], PC=args["PC"],
                RX=args["RX"], AZ=args["AZ"], BB=args["BB"], EE=args["EE"], ARC=args["ARC"]
            )

            db.session.add(novo)
            db.session.commit()

            # resposta 201 com JSON do objeto
            return jsonify({
                **novo.to_dict() if hasattr(novo, "to_dict") else {
                    "numeroSerie": novo.numeroSerie,
                    "data": novo.data,
                    "apostadoParcial": novo.apostadoParcial,
                    "taxaGanhoParcial": novo.taxaGanhoParcial,
                    "atribuidoParcial": novo.atribuidoParcial,
                    "Maquinas_numeroSerie": novo.Maquinas_numeroSerie,
                    "apostadoParcialDinheiro": novo.apostadoParcialDinheiro,
                    "VD": novo.VD, "PT": novo.PT, "CI": novo.CI, "AM": novo.AM,
                    "GM": novo.GM, "VR": novo.VR, "LR": novo.LR, "PC": novo.PC,
                    "RX": novo.RX, "AZ": novo.AZ, "BB": novo.BB, "EE": novo.EE, "ARC": novo.ARC
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("Erro ao criar levantamento")
            return {"error": str(e)}, 500
