from models import db
from sqlalchemy import CheckConstraint
from datetime import datetime

class LevantamentoModel(db.Model):
    __tablename__ = 'levantamentos'

    # Se este numeroSerie é o ID único do talão, deixa-o como PK
    numeroSerie = db.Column(db.String(64), primary_key=True)  # <— 64 para folga

    # usa DateTime; guarda sempre em UTC
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # métricas parciais (ajusta tipos ao teu domínio; sugiro cêntimos como int)
    apostadoParcial        = db.Column(db.Integer, nullable=False, default=0)
    taxaGanhoParcial       = db.Column(db.Float,   nullable=False, default=0.0)
    atribuidoParcial       = db.Column(db.Float,   nullable=False, default=0.0)
    apostadoParcialDinheiro= db.Column(db.Integer, nullable=False, default=0)  # <— ESTAVA EM FALTA

    # FK para máquinas (ajusta tamanho ao da tabela 'maquinas')
    Maquinas_numeroSerie = db.Column(
        db.String(32),  # <— usa o mesmo tamanho da coluna maquinas.numeroSerie
        db.ForeignKey('maquinas.numeroSerie'),
        nullable=False,
        index=True
    )

    # contadores por prémio — sempre >= 0
    VD  = db.Column(db.Integer, nullable=False, default=0)
    PT  = db.Column(db.Integer, nullable=False, default=0)
    CI  = db.Column(db.Integer, nullable=False, default=0)
    AM  = db.Column(db.Integer, nullable=False, default=0)
    GM  = db.Column(db.Integer, nullable=False, default=0)
    VR  = db.Column(db.Integer, nullable=False, default=0)
    LR  = db.Column(db.Integer, nullable=False, default=0)
    PC  = db.Column(db.Integer, nullable=False, default=0)
    RX  = db.Column(db.Integer, nullable=False, default=0)
    AZ  = db.Column(db.Integer, nullable=False, default=0)
    BB  = db.Column(db.Integer, nullable=False, default=0)
    EE  = db.Column(db.Integer, nullable=False, default=0)
    ARC = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (
        # cintos e suspensórios: evita negativos na BD
        CheckConstraint('VD  >= 0'),
        CheckConstraint('PT  >= 0'),
        CheckConstraint('CI  >= 0'),
        CheckConstraint('AM  >= 0'),
        CheckConstraint('GM  >= 0'),
        CheckConstraint('VR  >= 0'),
        CheckConstraint('LR  >= 0'),
        CheckConstraint('PC  >= 0'),
        CheckConstraint('RX  >= 0'),
        CheckConstraint('AZ  >= 0'),
        CheckConstraint('BB  >= 0'),
        CheckConstraint('EE  >= 0'),
        CheckConstraint('ARC >= 0'),
    )

    def __repr__(self):
        return f"<Levantamento(numeroSerie={self.numeroSerie}, Maquinas_numeroSerie={self.Maquinas_numeroSerie})>"
