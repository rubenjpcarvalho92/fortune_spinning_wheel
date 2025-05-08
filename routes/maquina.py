
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from models.maquina import MaquinaModel
from models.admin import AdminModel
from models.cliente import ClienteModel
from models.funcionario import FuncionarioModel
from models.login import LoginModel
from models import db
import logging

logger = logging.getLogger(__name__)

# Definir os campos de serialização
resource_fields_maquina = {
    'numeroSerie': fields.String,
    'valorAposta': fields.Integer,
    'apostadoParcialDinheiro': fields.Integer,
    'atribuidoTotal': fields.Float,
    'apostadoTotal': fields.Integer,
    'taxaGanhoDefinida': fields.Float,
    'taxaGanhoActual': fields.Float,
    'taxaGanhoParcial': fields.Float,
    'apostadoParcial': fields.Integer,
    'atribuidoParcial': fields.Float,
    'status': fields.String,
    'roloPapelOK': fields.String,
    'stockOK': fields.String,
    'Admins_NIF': fields.String,
    'Clientes_NIF': fields.String,
    'Funcionarios_NIF': fields.String,
    'MACArduino': fields.String
}

# Parser para criação de máquina
maquina_create_arg = reqparse.RequestParser()
maquina_create_arg.add_argument("numeroSerie", type=str, help="Número de série inválido.", required=True)
maquina_create_arg.add_argument("valorAposta", type=int, help="Valor da aposta inválido.", required=True)
maquina_create_arg.add_argument("apostadoParcialDinheiro", type=int, help="Valor da aposta em dinheiro inválido.", required=True)
maquina_create_arg.add_argument("atribuidoTotal", type=float, help="Valor total atribuído inválido.", required=True)
maquina_create_arg.add_argument("apostadoTotal", type=float, help="Valor total apostado inválido.", required=True)
maquina_create_arg.add_argument("taxaGanhoDefinida", type=float, help="Taxa de ganho definida inválida.", required=True)
maquina_create_arg.add_argument("taxaGanhoActual", type=float, help="Taxa de ganho atual inválida.", required=True)
maquina_create_arg.add_argument("taxaGanhoParcial", type=float, help="Taxa de ganho parcial inválida.", required=True)
maquina_create_arg.add_argument("apostadoParcial", type=int, help="Valor apostado parcial inválido.", required=True)
maquina_create_arg.add_argument("atribuidoParcial", type=float, help="Valor atribuído parcial inválido.", required=True)
maquina_create_arg.add_argument("status", type=str, help="Estado da máquina inválido.", required=True)
maquina_create_arg.add_argument("roloPapelOK", type=str, help="Status do rolo de papel inválido.", required=True)
maquina_create_arg.add_argument("stockOK", type=str, help="Status do estoque inválido.", required=True)
maquina_create_arg.add_argument("Admins_NIF", type=str, help="NIF do Admin associado é inválido.", required=False)
maquina_create_arg.add_argument("Clientes_NIF", type=str, help="NIF do Cliente associado é inválido.", required=False)
maquina_create_arg.add_argument("Funcionarios_NIF", type=str, help="NIF do Funcionário associado é inválido.", required=False)
maquina_create_arg.add_argument("MACArduino", type=str, help="MAC Address do Arduino", required=True)

# Parser para busca de máquina
maquina_get_arg = reqparse.RequestParser()
maquina_get_arg.add_argument("numeroSerie", type=str, help="Número de série é obrigatório.", required=True)

def validar_nif(model, nif, role):
    """
    Função auxiliar para validar se o NIF existe na tabela associada.
    """
    if nif:  # Apenas valida se o NIF foi fornecido
        registro = model.query.filter_by(NIF=nif).first()
        if not registro:
            abort(404, message=f"{role} com NIF {nif} não encontrado.")


class Maquina(Resource):
    @marshal_with(resource_fields_maquina)
    def get(self, numeroSerie):
        """
        GET: Busca uma máquina pelo número de série.
        """
        logger.info(f"Buscando máquina com número de série: {numeroSerie}")
        try:
            maquina = MaquinaModel.query.filter_by(numeroSerie=numeroSerie).first()
            if not maquina:
                logger.warning(f"Máquina com número de série {numeroSerie} não encontrada.")
                abort(404, message="Máquina não encontrada.")
            return maquina
        except Exception as e:
            logger.error(f"Erro ao buscar máquina com número de série {numeroSerie}: {str(e)}")
            abort(500, message="Erro interno ao buscar a máquina.")

    @marshal_with(resource_fields_maquina)
    def post(self,numeroSerie):
        """
        POST: Cria uma nova máquina.
        """
        args = maquina_create_arg.parse_args()
        try:
            logger.info(f"Tentando criar máquina com os dados: {args}")

            # Validar NIFs relacionados
            for role, model in [("Admin", AdminModel), ("Cliente", ClienteModel), ("Funcionário", FuncionarioModel)]:
                nif = args.get(f"{role}s_NIF")
                if nif:
                    validar_nif(model, nif, role)

            # Verificar se a máquina já existe
            if MaquinaModel.query.filter_by(numeroSerie=args['numeroSerie']).first():
                logger.warning(f"Máquina com número de série {args['numeroSerie']} já existe.")
                abort(409, message=f"Máquina com número de série {args['numeroSerie']} já existe.")

            nova_maquina = MaquinaModel(**args)
            db.session.add(nova_maquina)
            db.session.commit()

            logger.info(f"Máquina criada com sucesso: {nova_maquina}")
            return nova_maquina, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar máquina: {str(e)}")
            abort(500, message="Erro interno ao criar a máquina.")

    @marshal_with(resource_fields_maquina)
    def put(self, numeroSerie):
        """
        PUT: Atualiza os dados de uma máquina existente.
        """
        args = maquina_create_arg.parse_args()
        try:
            logger.info(f"Tentando atualizar máquina com número de série: {numeroSerie}")
            maquina = MaquinaModel.query.filter_by(numeroSerie=numeroSerie).first()
            if not maquina:
                logger.warning(f"Máquina com número de série {numeroSerie} não encontrada.")
                abort(404, message=f"Máquina com número de série {numeroSerie} não encontrada.")

            # Atualizar os campos
            for key, value in args.items():
                setattr(maquina, key, value)
            db.session.commit()

            logger.info(f"Máquina atualizada com sucesso: {maquina}")
            return maquina, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar máquina com número de série {numeroSerie}: {str(e)}")
            abort(500, message="Erro interno ao atualizar a máquina.")
