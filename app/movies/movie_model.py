from flask import url_for


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.String(16))
    rating = db.Column(db.Integer)
    photo_url = db.Column(db.String(256))
    movie_url = db.Column(db.String(256))
    subtitles_url = db.Column(db.String(256))
    genre = db.Column(db.String(256))
    producer = db.Column(db.String(64))
    director = db.Column(db.String(64))
    actors = db.Column(db.String(256))
    country = db.Column(db.String(128))
    
    def import_data(self, data):
        try:
            for key, value in data.items():
                setattr(self, key, value)
        except KeyError as e:
            raise ValidationError('Invalid movie: missing ' + e.args[0])
        return self
    
    def get_self_url(self):
        return url_for('watch', id=self.id,
                       title=self.title, _external=True)
    
    def get_search_item(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'rating': self.rating,
            'photo_url': self.photo_url,
            'self_url': self.get_self_url(),
            'genre': self.genre
        }
    
    def get_watch_item(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'rating': self.rating,
            'photo_url': self.photo_url,
            'movie_url': self.movie_url,
            'subtitles_url': self.subtitles_url,
            'self_url': self.get_self_url(),
            'genre': self.genre,
            'producer': self.producer,
            'director': self.director,
            'actors': self.actors,
            'country': self.country
        }
