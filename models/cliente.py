from models import db

class ClienteModel(db.Model):
    __tablename__ = "clientes"

    NIF = db.Column(db.String(9), primary_key=True)
    nomeCliente = db.Column(db.String(45))
    passwordCliente = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Cliente(NIF={self.NIF}, nomeCliente='{self.nomeCliente}',passwordCliente='(self.passwordCliente)')>"
