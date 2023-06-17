# haku/models/community.py

from haku import db
from datetime import datetime

class Community(db.Model):
    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='community', lazy=True)