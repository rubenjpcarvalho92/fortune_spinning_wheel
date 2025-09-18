from models import db

class LevantamentoModel(db.Model):
    __tablename__ = 'levantamentos'

    # PK: a tua BD está com VARCHAR(32)
    numeroSerie = db.Column(db.String(32), primary_key=True)

    # Manténs como string (VARCHAR(46) na BD)
    data = db.Column(db.String(46), nullable=True)

    # Métricas
    apostadoParcial         = db.Column(db.Integer, nullable=True)
    taxaGanhoParcial        = db.Column(db.Float(precision=2), nullable=True)  # double(15,2) na BD
    atribuidoParcial        = db.Column(db.Float, nullable=True)

    # *** ESTE CAMPO É O QUE FALTAVA NO MODELO ***
    apostadoParcialDinheiro = db.Column(db.Integer, nullable=False, default=0)

    # FK/index (na tua BD está VARCHAR(16) e pode ser NULL)
    Maquinas_numeroSerie    = db.Column(db.String(16), index=True, nullable=True)

    # Contadores
    VD  = db.Column(db.Integer, nullable=True)
    PT  = db.Column(db.Integer, nullable=True)
    CI  = db.Column(db.Integer, nullable=True)
    AM  = db.Column(db.Integer, nullable=True)
    GM  = db.Column(db.Integer, nullable=True)
    VR  = db.Column(db.Integer, nullable=True)
    LR  = db.Column(db.Integer, nullable=True)
    PC  = db.Column(db.Integer, nullable=True)
    RX  = db.Column(db.Integer, nullable=True)
    AZ  = db.Column(db.Integer, nullable=True)
    BB  = db.Column(db.Integer, nullable=True)
    EE  = db.Column(db.Integer, nullable=True)
    ARC = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Levantamento(numeroSerie={self.numeroSerie}, Maquinas_numeroSerie={self.Maquinas_numeroSerie})>"

    def to_dict(self):
        return {
            "numeroSerie": self.numeroSerie,
            "data": self.data,
            "apostadoParcial": self.apostadoParcial,
            "taxaGanhoParcial": self.taxaGanhoParcial,
            "atribuidoParcial": self.atribuidoParcial,
            "apostadoParcialDinheiro": self.apostadoParcialDinheiro,
            "Maquinas_numeroSerie": self.Maquinas_numeroSerie,
            "VD": self.VD, "PT": self.PT, "CI": self.CI, "AM": self.AM,
            "GM": self.GM, "VR": self.VR, "LR": self.LR, "PC": self.PC,
            "RX": self.RX, "AZ": self.AZ, "BB": self.BB, "EE": self.EE, "ARC": self.ARC
        }
