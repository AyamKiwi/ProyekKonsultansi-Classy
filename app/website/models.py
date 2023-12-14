from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class Matkul(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ruangan = db.Column(db.String(10000))
    tanggal = db.Column(db.DateTime())

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nim = db.Column(db.String(7), unique = True)
    password = db.Column(db.String(100))