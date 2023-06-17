from haku import db

class SubredditPost(db.Model):
    __tablename__ = 'subreddit_posts'

    id = db.Column(db.Integer, primary_key=True)
    subreddit_id = db.Column(db.Integer, db.ForeignKey('subreddits.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
