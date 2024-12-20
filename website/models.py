from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Create classes to see wrapped from specific times in your life
class Wrapped(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artists_rel = db.relationship('Artists')
    tracks_rel = db.relationship('Tracks')
    
class Artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_term = db.Column(db.String(500))
    medium_term = db.Column(db.String(500))
    long_term = db.Column(db.String(500))
    wrapped_id = db.Column(db.Integer, db.ForeignKey('wrapped.id'))
    
class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_term = db.Column(db.String(500))
    medium_term = db.Column(db.String(500))
    long_term = db.Column(db.String(500))
    wrapped_id = db.Column(db.Integer, db.ForeignKey('wrapped.id'))
    
# create database model, define the schema
# store in the object
# inherit db.model (like a blueprint) and UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    f_name = db.Column(db.String(150))
    wrappeds = db.relationship('Wrapped')