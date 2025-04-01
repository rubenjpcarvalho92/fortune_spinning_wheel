from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
api = Api(app)

#DB Connection
#Old DB connectyion
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#ligação bas de dados
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///root:password@server.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:1000/test'

db = SQLAlchemy(app)
#db.create_all()



class MaquinaModel(db.Model):
	 id=db.Column(db.Integer, primary_key=True)
	 estado = db.Column(db.String(100), nullable=True)
	 ganho_pretendido = db.Column(db.Float, nullable=False)
	 ganho_actual = db.Column(db.Float, nullable=False)
	 morada = db.Column(db.String(100), nullable=False)
	 cliente = db.Column(db.String(100), nullable=False)
	 valor_total_apostado = db.Column(db.Float, nullable=False)
	 valor_total_premios = db.Column(db.Float, nullable=False)


	 def __repr__(self):
	 	return f"Maquina(estado = {estado}, ganho_pretendido = {ganho_pretendido}, ganho_actual = {ganho_actual}, morada = {morada}, cliente = {cliente}, numero_serie = {numero_serie}, valor_total_apostado = {valor_total_apostado}, valor_total_premios = {valor_total_premios})"

#Parser input
cliente_create_arg = reqparse.RequestParser()
cliente_create_arg.add_argument("estado", type=str, help="Estado inválida", required=True)
cliente_create_arg.add_argument("ganho_pretendido", type=float, help="Ganho pretendido inválido", required=True)
cliente_create_arg.add_argument("ganho_actual", type=float, help="Ganho actual inválido", required=True)
cliente_create_arg.add_argument("morada", type=str, help="Morada inválida", required=True)
cliente_create_arg.add_argument("cliente", type=str, help="Cliente inválido", required=True)
cliente_create_arg.add_argument("valor_total_apostado", type=float, help="Valor total apostado inválido", required=True)
cliente_create_arg.add_argument("valor_total_premios", type=float, help="Valor total valor_total_premios inválido", required=True)


resource_fields = {
     'id' : fields.Integer,
	'estado': fields.String,
	'ganho_pretendido': fields.Float,
	'ganho_actual': fields.Float,
	'morad 

##Error Handling
#def abort_arduino_id_invalid(arduino_id):
#	if arduino_id not in listas:
#		abort(404, message="Arduino não registado")
#
#
#def abort_arduino_id_exists(arduino_id):
#	if arduino_id in listas:
#		abort(409, message="Arduino já registado")
#
class Maquina(Resource):
	#isto serve então para faser a serialização do resultado tendo em conta o que está definido no resourse_fields
	@marshal_with(resource_fields)
	def get (self,numero_serie):
		#abort_arduino_id_invalid(arduino_id)
		#return listas[arduino_id]
		result = MaquinaModel.query.filter_by(id=numero_serie).first()
		if not result:
			abort(404,  message="Não encoontra a maquina com esse id...")

		# O que é returnado acabaa por vir numa estrutura que depois precisa de ter uma especie de parser e dai a criação do resource

		return result

	@marshal_with(resource_fields)
	def put(self,numero_serie):
		#lista = ListaModel 
		args = cliente_create_arg.parse_args()
		result = MaquinaModel.query.filter_by(id=numero_serie).first()
		if result: 
			abort(409,  message="Maquina já registada...")

		maquina = MaquinaModel(id=numero_serie, ganho_pretendido=args['ganho_pretendido'], ganho_actual=args['ganho_actual'], morada=args['morada'], cliente=args['cliente'], valor_total_apostado=args['valor_total_apostado'], valor_total_premios=args['valor_total_premios'], estado=args['estado'])
		db.session.add(maquina)
		db.session.commit()
		#listas[arduino_id] = args
		return maquina, 201

api.add_resource(Maquina, "/maquinas/<int:numero_serie>")

if __name__ == "__main__":
	app.run(debug=True)