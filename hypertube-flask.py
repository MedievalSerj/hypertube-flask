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
        

@app.route('/search/<int:start>/<int:stop>')
def search(start, stop):
    pass


@app.route('/watch/<int:id>/<string:title>')
def watch(id, title):
    pass

    
if __name__ == '__main__':
    db.create_all()
    app.run()
