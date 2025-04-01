from models import db

class LevantamentoModel(db.Model):
    __tablename__ = 'levantamentos'

    numeroSerie = db.Column(db.String(30), primary_key=True)
    data = db.Column(db.String(46))
    apostadoParcial = db.Column(db.Integer)
    taxaGanhoParcial = db.Column(db.Float)
    atribuidoParcial = db.Column(db.Float)
    Maquinas_numeroSerie = db.Column(db.String(16), db.ForeignKey('maquinas.numeroSerie'))

    VD = db.Column(db.Integer)
    PT = db.Column(db.Integer)
    CI = db.Column(db.Integer)
    AM = db.Column(db.Integer)
    GM = db.Column(db.Integer)
    VR = db.Column(db.Integer)
    LR = db.Column(db.Integer)
    PC = db.Column(db.Integer)
    RX = db.Column(db.Integer)
    AZ = db.Column(db.Integer)
    BB = db.Column(db.Integer)
    EE = db.Column(db.Integer)
    ARC = db.Column(db.Integer)

    def __repr__(self):
        return f"<Levantamento(numeroSerie={self.numeroSerie}, Maquinas_numeroSerie={self.Maquinas_numeroSerie})>"
