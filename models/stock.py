from models import db

class StockModel(db.Model):
    __tablename__ = 'stocks'
    Maquinas_numeroSerie = db.Column(db.String, primary_key=True)
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
        return (f"<Stock(Maquinas_numeroSerie={self.Maquinas_numeroSerie}, "
                f"VD={self.VD}, PT={self.PT}, CI={self.CI}, "
                f"AM={self.AM}, GM={self.GM}, VR={self.LR}, "
                f"PC={self.PC}, RX={self.RX}, AZ={self.AZ}, "
                f"BB={self.BB}, EE={self.EE}, ARC={self.ARC})>")
