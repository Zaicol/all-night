from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("app")
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all-night.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/static/img'
db = SQLAlchemy(app)


class UsersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    isOrg = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    regdate = db.Column(db.DateTime, unique=False, nullable=False)
    av_type = db.Column(db.String(4), unique=False,
                        nullable=False, default='png')


class PlaceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)
    lat = db.Column(db.String(20), unique=False, nullable=False)
    lon = db.Column(db.String(20), unique=False, nullable=False)
    pic = db.Column(db.String(20), unique=False, nullable=True)
    date = db.Column(db.DateTime, unique=False, nullable=True)
    author = db.Column(db.Integer, unique=False, nullable=False)
