from models import db

class FuncionarioModel(db.Model):
    __tablename__ = "funcionarios"

    NIF = db.Column(db.String(9), primary_key=True)
    nomeFuncionario = db.Column(db.String(45))
    passwordFuncionario = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Funcionario(NIF={self.NIF}, nomeFuncionario='{self.nomeFuncionario}')>"
