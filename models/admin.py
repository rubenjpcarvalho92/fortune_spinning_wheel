from models import db

class AdminModel(db.Model):
    __tablename__ = "admins"

    NIF = db.Column(db.String(9), primary_key=True)
    nomeAdmin = db.Column(db.String(45))
    passwordAdmin = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Admin(NIF={self.NIF}, nomeAdmin='{self.nomeAdmin}')>"
