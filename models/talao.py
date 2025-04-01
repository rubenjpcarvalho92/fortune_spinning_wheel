from models import db

class TalaoModel(db.Model):
    __tablename__ = "taloes"

    numeroSerie = db.Column(db.String(30), primary_key=True)  # Identificador único do talão
    numeroJogadas = db.Column(db.Integer)
    valorJogadas = db.Column(db.Integer)
    dataImpressao = db.Column(db.String(30), nullable=True)
    impressaoOK = db.Column(db.Boolean)
    Maquinas_numeroSerie = db.Column(db.String(16), db.ForeignKey("maquinas.numeroSerie"), nullable=False)

    def __repr__(self):
        return (f"<Talao(numeroSerie={self.numeroSerie}, "
                f"numeroJogadas={self.numeroJogadas}, "
                f"valorJogadas={self.valorJogadas}, "
                f"dataImpressao={self.dataImpressao}, "
                f"impressaoOK={self.impressaoOK}, "
                f"Maquinas_numeroSerie={self.Maquinas_numeroSerie})>")
