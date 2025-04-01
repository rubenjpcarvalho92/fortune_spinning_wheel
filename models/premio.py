from models import db
from datetime import datetime

class PremioModel(db.Model):
    __tablename__ = "premios"  # Nome da tabela no banco de dados

    numeroSerie = db.Column(db.String(36), primary_key=True)  # Identificador único do prêmio
    codigoRoleta = db.Column(db.String(2), nullable=False)
    data = db.Column(db.String, nullable=False, primary_key=True)
    categoriaPremio = db.Column(db.Float)
    contabilizado = db.Column(db.Integer)
    Taloes_numeroSerie = db.Column(db.String(30), db.ForeignKey("taloes.numeroSerie"), nullable=True)
    
    # Relacionamentos (opcional)
    talao = db.relationship("TalaoModel", backref="premios")


    def __repr__(self):
        return (f"<Premio(numeroSerie={self.numeroSerie}, "
                f"codigoRoleta={self.codigoRoleta}, "
                f"data={self.data}, "
                f"categoriaPremio={self.categoriaPremio}, contabilizado={self.contabilizado}"
                f"Taloes_numeroSerie={self.Taloes_numeroSerie})>")

