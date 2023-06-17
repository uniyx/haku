from haku import db
from sqlalchemy.sql import func

class Subreddit(db.Model):
    __tablename__ = 'subreddits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
