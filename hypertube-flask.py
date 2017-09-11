#!/usr/bin/env python
import os
from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data.sqlite')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)


class ValidationError(ValueError):
    pass


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
        

@app.route('/add', methods=['POST'])
def add_movie():
    movie = Movie()
    movie.import_data(request.json)
    db.session.add(movie)
    db.session.commit()
    return jsonify({}), 201, {'Location': movie.get_self_url()}


@app.route('/get_one/<int:id>')
def get_one(id):
    return jsonify(Movie.query.get_or_404(id).get_search_item())


@app.route('/search/<int:start>/<int:stop>')
def search(start, stop):
    all = [m.get_search_item() for m in Movie.query.all()]
    return jsonify({'search_results': all[start:stop]})


@app.route('/watch/<int:id>')
def watch(id):
    return jsonify(Movie.query.get_or_404(id).get_watch_item())

    
if __name__ == '__main__':
    db.create_all()
    movies = []
    if False:
        try:
            movies.append({
                'id': 1,
                'title': 'Movie 1',
                'year': 1968,
                'rating': 100500,
                'photo_url': '/static/movies/movie_1/movie_1.png',
                'movie_url': '/static/movies/movie_1/movie_1.mkv',
                'subtitles_url': '/static/movies/movie_1/movie_1.srt',
                'genre': 'Comedy',
                'producer': 'Don Jownes',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'country': 'Paragvay'
            })
            movies.append({
                'id': 2,
                'title': 'Movie 2',
                'year': 1968,
                'rating': 100500,
                'photo_url': '/static/movies/movie_2/movie_2.png',
                'movie_url': '/static/movies/movie_2/movie_2.mkv',
                'subtitles_url': '/static/movies/movie_2/movie_2.srt',
                'genre': 'Comedy',
                'producer': 'Don Jownes',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'country': 'Paragvay'
            })
            movies.append({
                'id': 3,
                'title': 'Movie 3',
                'year': 1968,
                'rating': 100500,
                'photo_url': '/static/movies/movie_3/movie_3.png',
                'movie_url': '/static/movies/movie_3/movie_3.mkv',
                'subtitles_url': '/static/movies/movie_3/movie_3.srt',
                'genre': 'Comedy',
                'producer': 'Don Jownes',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'country': 'Paragvay'
            })
            movies.append({
                'id': 4,
                'title': 'Movie 4',
                'year': 1968,
                'rating': 100500,
                'photo_url': '/static/movies/movie_4/movie_4.jpg',
                'movie_url': '/static/movies/movie_4/movie_4.mkv',
                'subtitles_url': '/static/movies/movie_4/movie_4.srt',
                'genre': 'Comedy',
                'producer': 'Don Jownes',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'country': 'Paragvay'
            })
            movies.append({
                'id': 5,
                'title': 'Movie 5',
                'year': 1968,
                'rating': 100500,
                'photo_url': '/static/movies/movie_5/movie_5.png',
                'movie_url': '/static/movies/movie_5/movie_5.mkv',
                'subtitles_url': '/static/movies/movie_5/movie_5.srt',
                'genre': 'Comedy',
                'producer': 'Don Jownes',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'country': 'Paragvay'
            })
            movies.append({
                'id': 6,
                'title': 'Movie 6',
                'year': 1968,
                'rating': 100500,
                'photo_url': '/static/movies/movie_6/movie_6.jpg',
                'movie_url': '/static/movies/movie_6/movie_6.mkv',
                'subtitles_url': '/static/movies/movie_6/movie_6.srt',
                'genre': 'Comedy',
                'producer': 'Don Jownes',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'country': 'Paragvay'
            })
            movies.append({
                'id': 7,
                'title': 'Movie 7',
                'year': 1968,
                'rating': 100500,
                'photo_url': '/static/movies/movie_7/movie_7.jpg',
                'movie_url': '/static/movies/movie_7/movie_7.mkv',
                'subtitles_url': '/static/movies/movie_7/movie_7.srt',
                'genre': 'Comedy',
                'producer': 'Don Jownes',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'country': 'Paragvay'
            })
            for movie in movies:
                movie_object = Movie()
                movie_object.import_data(movie)
                db.session.add(movie_object)
                db.session.commit()
        except Exception as e:
            pass
    app.run()
