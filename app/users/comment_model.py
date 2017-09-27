import datetime
from flask import url_for
from ..exceptions import ValidationError


class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    msg = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    def get_url(self):
        return url_for('get_all_comments', movie_id=self.movie_id)
    
    def export_data(self):
        return {
            "movie_id": self.movie_id,
            "user_id": self.user_id,
            "msg": self.msg,
            "date_time": self.date_time
        }
    
    def import_data(self, data):
        try:
            self.movie_id = data['movie_id']
            self.user_id = data['user_id']
            self.msg = data['msg']
        except KeyError as e:
            raise ValidationError('Invalid msg: missing ' + e.args[0])
