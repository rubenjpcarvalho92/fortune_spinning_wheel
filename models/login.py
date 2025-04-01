from models import db

from datetime import datetime
from sqlalchemy import ForeignKey

class LoginModel(db.Model):
    __tablename__ = "logins"

    dataLogin = db.Column(db.String, nullable=False, primary_key=True,)
    nivelAcesso = db.Column(db.String(45), nullable=False)
    NIF = db.Column(db.Integer, nullable=False)
    resultado = db.Column(db.String, nullable=False)
    Maquinas_numeroSerie = db.Column(db.String, nullable=True)

    def __repr__(self):
        return (f"<Login(dataLogin={self.dataLogin}, "
                f"nivelAcesso='{self.nivelAcesso}', NIF={self.NIF}, resultado= {self.resultado} "
                f"Maquina_numeroSerie={self.Maquinas_numeroSerie})>")
