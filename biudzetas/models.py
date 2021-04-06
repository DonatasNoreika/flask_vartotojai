from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from biudzetas import app, db

class Vartotojas(db.Model, UserMixin):
    def ar_admin(self):
        vartotojai = Vartotojas.query.all()
        return len(vartotojai) < 1

    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True, nullable=False)
    nuotrauka = db.Column(db.String(20), nullable=False, default='default.jpg')
    slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)
    admin = db.Column("Administratorius", db.Boolean, default=ar_admin)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Vartotojas.query.get(user_id)


class Irasas(db.Model):
    __tablename__ = "irasas"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column("Data", db.DateTime, default=datetime.now())
    pajamos = db.Column("Pajamos", db.Boolean)
    suma = db.Column("Vardas", db.Integer)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey("vartotojas.id"))
    vartotojas = db.relationship("Vartotojas", lazy=True)


