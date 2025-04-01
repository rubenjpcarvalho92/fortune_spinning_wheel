from flask_restful import Resource, reqparse, marshal_with, fields, abort
from models.setup import SetupModel
from models.maquina import MaquinaModel
from models import db
import logging

logger = logging.getLogger(__name__)

# 🔹 Campos para serialização
resource_fields_setup = {
    'Maquinas_numeroSerie': fields.String
}

# 🔹 Adiciona dinamicamente os campos da roleta
for i in range(16):
    resource_fields_setup[f'P{i}'] = fields.Float
    resource_fields_setup[f'L{i}'] = fields.String
    resource_fields_setup[f'C{i}'] = fields.String


# 🔹 Adiciona brindes
for brinde in ['am', 'az', 'bb', 'ci', 'ee', 'gm', 'lr', 'pc', 'pt', 'rx', 'vd', 'vr', 'arc']:
    resource_fields_setup[f'brinde_{brinde}'] = fields.String

# 🔹 Parser para criar ou atualizar setups
setup_create_arg = reqparse.RequestParser()
setup_create_arg.add_argument("Maquinas_numeroSerie", type=str, required=True, help="Número de série da máquina é obrigatório.")

for i in range(16):
    setup_create_arg.add_argument(f"P{i}", type=float, required=True)
    setup_create_arg.add_argument(f"L{i}", type=str, required=True)
    setup_create_arg.add_argument(f"C{i}", type=str, required=True)

for brinde in ['am', 'az', 'bb', 'ci', 'ee', 'gm', 'lr', 'pc', 'pt', 'rx', 'vd', 'vr', 'arc']:
    setup_create_arg.add_argument(f"brinde_{brinde}", type=str, required=False)

# 🔹 Classe Setup
class Setup(Resource):
    @marshal_with(resource_fields_setup)
    def get(self, Maquinas_numeroSerie):
        logger.info(f"Buscando setup da máquina com número de série {Maquinas_numeroSerie}")
        setup = SetupModel.query.filter_by(Maquinas_numeroSerie=Maquinas_numeroSerie).first()
        if not setup:
            logger.warning(f"Setup para máquina {Maquinas_numeroSerie} não encontrado.")
            abort(404, message="Setup não encontrado para esta máquina.")
        return setup

    @marshal_with(resource_fields_setup)
    def post(self):
        args = setup_create_arg.parse_args()
        try:
            maquina = MaquinaModel.query.get(args['Maquinas_numeroSerie'])
            if not maquina:
                abort(404, message=f"Máquina com número de série {args['Maquinas_numeroSerie']} não encontrada.")

            if SetupModel.query.filter_by(Maquinas_numeroSerie=args['Maquinas_numeroSerie']).first():
                abort(409, message=f"Setup já existe para a máquina {args['Maquinas_numeroSerie']}.")

            setup = SetupModel(**args)
            db.session.add(setup)
            db.session.commit()
            logger.info(f"Setup criado com sucesso para a máquina {args['Maquinas_numeroSerie']}.")
            return setup, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar setup: {str(e)}")
            abort(500, message="Erro interno ao criar setup.")

    @marshal_with(resource_fields_setup)
    def put(self, Maquinas_numeroSerie):
        args = setup_create_arg.parse_args()
        try:
            setup = SetupModel.query.filter_by(Maquinas_numeroSerie=Maquinas_numeroSerie).first()
            if not setup:
                abort(404, message="Setup não encontrado para esta máquina.")

            for key, value in args.items():
                if value is not None:
                    setattr(setup, key, value)

            db.session.commit()
            logger.info(f"Setup atualizado com sucesso para a máquina {Maquinas_numeroSerie}.")
            return setup, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar setup: {str(e)}")
            abort(500, message="Erro interno ao atualizar setup.")

    def delete(self, Maquinas_numeroSerie):
        try:
            setup = SetupModel.query.filter_by(Maquinas_numeroSerie=Maquinas_numeroSerie).first()
            if not setup:
                abort(404, message="Setup não encontrado para esta máquina.")

            db.session.delete(setup)
            db.session.commit()
            logger.info(f"Setup removido com sucesso para a máquina {Maquinas_numeroSerie}.")
            return {"message": "Setup removido com sucesso."}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir setup: {str(e)}")
            abort(500, message="Erro interno ao excluir setup.")
