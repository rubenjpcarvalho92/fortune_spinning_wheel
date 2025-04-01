from sqlalchemy import Column, Float, String, ForeignKey
from models import db


class SetupModel(db.Model):
    __tablename__ = "setups"

    Maquinas_numeroSerie = db.Column(String, ForeignKey("maquinas.numeroSerie"), primary_key=True)

    # Campos da roleta (P, L, C)
    P0 = db.Column(Float);  L0 = db.Column(String); C0 = db.Column(String)
    P1 = db.Column(Float);  L1 = db.Column(String); C1 = db.Column(String)
    P2 = db.Column(Float);  L2 = db.Column(String); C2 = db.Column(String)
    P3 = db.Column(Float);  L3 = db.Column(String); C3 = db.Column(String)
    P4 = db.Column(Float);  L4 = db.Column(String); C4 = db.Column(String)
    P5 = db.Column(Float);  L5 = db.Column(String); C5 = db.Column(String)
    P6 = db.Column(Float);  L6 = db.Column(String); C6 = db.Column(String)
    P7 = db.Column(Float);  L7 = db.Column(String); C7 = db.Column(String)
    P8 = db.Column(Float);  L8 = db.Column(String); C8 = db.Column(String)
    P9 = db.Column(Float);  L9 = db.Column(String); C9 = db.Column(String)
    P10 = db.Column(Float); L10 = db.Column(String); C10 = db.Column(String)
    P11 = db.Column(Float); L11 = db.Column(String); C11 = db.Column(String)
    P12 = db.Column(Float); L12 = db.Column(String); C12 = db.Column(String)
    P13 = db.Column(Float); L13 = db.Column(String); C13 = db.Column(String)
    P14 = db.Column(Float); L14 = db.Column(String); C14 = db.Column(String)
    P15 = db.Column(Float); L15 = db.Column(String); C15 = db.Column(String)

    # Brindes (13)
    brinde_am = db.Column(String)
    brinde_az = db.Column(String)
    brinde_bb = db.Column(String)
    brinde_ci = db.Column(String)
    brinde_ee = db.Column(String)
    brinde_gm = db.Column(String)
    brinde_lr = db.Column(String)
    brinde_pc = db.Column(String)
    brinde_pt = db.Column(String)
    brinde_rx = db.Column(String)
    brinde_vd = db.Column(String)
    brinde_vr = db.Column(String)
    brinde_arc = db.Column(String)

    def __repr__(self):
        partes = [f"Maquinas_numeroSerie='{self.Maquinas_numeroSerie}'"]
        for i in range(16):
            partes.append(f"P{i}={getattr(self, f'P{i}', None)}")
            partes.append(f"L{i}={repr(getattr(self, f'L{i}', None))}")
            partes.append(f"C{i}={repr(getattr(self, f'C{i}', None))}")
        for key in [
            "brinde_am", "brinde_az", "brinde_bb", "brinde_ci", "brinde_ee", "brinde_gm", "brinde_lr",
            "brinde_pc", "brinde_pt", "brinde_rx", "brinde_vd", "brinde_vr", "brinde_arc"
        ]:
            partes.append(f"{key}={repr(getattr(self, key, None))}")
        return f"<Setup({', '.join(partes)})>"
