from flask_restful import Resource, reqparse, marshal_with, fields, abort
from models.stock import StockModel
from models import db
import logging

logger = logging.getLogger(__name__)

# Campos para serialização do recurso Stock
resource_fields_stock = {
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
    'ARC': fields.Integer,
    'Maquinas_numeroSerie': fields.String
}

# Parser para criação/atualização de stock
stock_create_update_arg = reqparse.RequestParser()
stock_create_update_arg.add_argument("VD", type=int, required=True, help="Valor para VD é obrigatório.")
stock_create_update_arg.add_argument("PT", type=int, required=True, help="Valor para PT é obrigatório.")
stock_create_update_arg.add_argument("CI", type=int, required=True, help="Valor para CI é obrigatório.")
stock_create_update_arg.add_argument("AM", type=int, required=True, help="Valor para AM é obrigatório.")
stock_create_update_arg.add_argument("GM", type=int, required=True, help="Valor para GM é obrigatório.")
stock_create_update_arg.add_argument("VR", type=int, required=True, help="Valor para VR é obrigatório.")
stock_create_update_arg.add_argument("LR", type=int, required=True, help="Valor para LR é obrigatório.")
stock_create_update_arg.add_argument("PC", type=int, required=True, help="Valor para PC é obrigatório.")
stock_create_update_arg.add_argument("RX", type=int, required=True, help="Valor para RX é obrigatório.")
stock_create_update_arg.add_argument("AZ", type=int, required=True, help="Valor para AZ é obrigatório.")
stock_create_update_arg.add_argument("BB", type=int, required=True, help="Valor para BB é obrigatório.")
stock_create_update_arg.add_argument("EE", type=int, required=True, help="Valor para EE é obrigatório.")
stock_create_update_arg.add_argument("ARC", type=int, required=True, help="Valor para ARC é obrigatório.")
stock_create_update_arg.add_argument("Maquinas_numeroSerie", type=str, required=True, help="Número de série da máquina é obrigatório.")

# Parser para busca de stock
stock_get_arg = reqparse.RequestParser()
stock_get_arg.add_argument("Maquinas_numeroSerie", type=str, required=True, help="Número de série da máquina é obrigatório.")

class Stock(Resource):
    @marshal_with(resource_fields_stock)
    def get(self, Maquinas_numeroSerie):
        try:
            stock = StockModel.query.filter_by(Maquinas_numeroSerie=Maquinas_numeroSerie).first()
            if not stock:
                abort(404, message=f"Stock para máquina {Maquinas_numeroSerie} não encontrado.")
            return stock
        except Exception as e:
            logger.error(f"Erro ao buscar stock: {str(e)}")
            abort(500, message="Erro interno ao buscar o stock.")

    @marshal_with(resource_fields_stock)
    def put(self, Maquinas_numeroSerie):
        args = stock_create_update_arg.parse_args()
        try:
            stock = StockModel.query.filter_by(Maquinas_numeroSerie=args['Maquinas_numeroSerie']).first()
            if stock:
                # Atualizar os valores existentes
                for field in ['VD', 'PT', 'CI', 'AM', 'GM', 'VR', 'LR', 'PC', 'RX', 'AZ', 'BB', 'EE', 'ARC']:
                    setattr(stock, field, args[field])
                logger.info(f"Stock atualizado: {stock}")
            else:
                # Criar novo stock
                stock = StockModel(**args)
                db.session.add(stock)
                logger.info(f"Novo stock criado: {stock}")

            db.session.commit()
            return stock, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar/atualizar stock: {str(e)}")
            abort(500, message="Erro interno ao criar/atualizar o stock.")

    @marshal_with(resource_fields_stock)
    def post(self):
        args = stock_create_update_arg.parse_args()
        try:
            # Criar novo stock sem verificar existência
            stock = StockModel(
                VD=args['VD'], PT=args['PT'], CI=args['CI'], AM=args['AM'],
                GM=args['GM'], VR=args['VR'], LR=args['LR'], PC=args['PC'],
                RX=args['RX'], AZ=args['AZ'], BB=args['BB'], EE=args['EE'],
                ARC=args['ARC'], Maquinas_numeroSerie=args['Maquinas_numeroSerie']
            )
            db.session.add(stock)
            db.session.commit()
            logger.info(f"Novo stock criado: {stock}")
            return stock, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar stock: {str(e)}")
            abort(500, message="Erro interno ao criar o stock.")
