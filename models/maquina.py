from models import db

from sqlalchemy import ForeignKey

class MaquinaModel(db.Model):
    __tablename__ = "maquinas"

    numeroSerie = db.Column(db.String(8), primary_key=True)  # Identificador único da máquina
    valorAposta = db.Column(db.Integer)
    atribuidoTotal = db.Column(db.Float)
    apostadoTotal = db.Column(db.Integer)
    taxaGanhoDefinida = db.Column(db.Float)
    taxaGanhoActual = db.Column(db.Float)
    taxaGanhoParcial = db.Column(db.Float)
    apostadoParcial = db.Column(db.Float)
    atribuidoParcial = db.Column(db.Float)
    status = db.Column(db.String(45))  # Comprimento do campo VARCHAR definido como 45
    roloPapelOK = db.Column(db.String(45))
    stockOK = db.Column(db.String(45))
    MACArduino = db.Column(db.String(17))
    # Chaves estrangeiras
    Admins_NIF = db.Column(db.String(9), db.ForeignKey("admins.NIF"), nullable=True)
    Clientes_NIF = db.Column(db.String(9), db.ForeignKey("clientes.NIF"), nullable=True)
    Funcionarios_NIF = db.Column(db.String(9), db.ForeignKey("funcionarios.NIF"), nullable=True)

    # Relacionamentos (opcional)
    admin = db.relationship("AdminModel", backref="maquinas")
    cliente = db.relationship("ClienteModel", backref="maquinas")
    funcionario = db.relationship("FuncionarioModel", backref="maquinas")
    talao = db.relationship("TalaoModel", backref="maquina", lazy=True)

    def __repr__(self):
        return (f"<Maquina(numeroSerie={self.numeroSerie}, valorAposta={self.valorAposta}, "
                f"atribuidoTotal={self.atribuidoTotal}, apostadoTotal={self.apostadoTotal}, "
                f"taxaGanhoDefinida={self.taxaGanhoDefinida}, taxaGanhoActual={self.taxaGanhoActual}, "
                f"taxaGanhoParcial={self.taxaGanhoParcial}, apostadoParcial={self.apostadoParcial}, "
                f"atribuidoParcial={self.atribuidoParcial}, status='{self.status}', "
                f"roloPapelOK={self.roloPapelOK}, stockOK={self.stockOK}, Admins_NIF={self.Admins_NIF}, "
                f"Clientes_NIF={self.Clientes_NIF}, Funcionarios_NIF={self.Funcionarios_NIF}, MACArduino={self.MACArduino})>")
