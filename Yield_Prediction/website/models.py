from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement =True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Match', backref='user', passive_deletes=True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement =True)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    matchid = db.Column(db.Integer)
    prop = db.Column(db.String)
    input = db.Column(db.String)
    curr_data = db.Column(db.Float)
    type = db.Column(db.String)
    threshold = db.Column(db.Integer)
    resolved = db.Column(db.Boolean)
    over_number = db.Column(db.Integer)
    result = db.Column(db.Boolean)



