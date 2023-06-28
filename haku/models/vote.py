# haku/models/vote.py

from haku import db

class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    value = db.Column(db.Integer, nullable=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    post = db.relationship('Post', backref=db.backref('vote_records', lazy=True))

    def __init__(self, user_id, post_id, value):
        self.user_id = user_id
        self.post_id = post_id
        self.value = value
