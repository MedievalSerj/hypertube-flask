#!/usr/bin/env python
from app import create_app
from app import db
import os
import sys
from app.users.user_model import User
from app.movies.movie_model import Movie


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cfg = sys.argv[1]
    else:
        cfg = 'development'
    app = create_app(cfg)
    if not os.path.exists('./app/static/users'):
        os.mkdir('./app/static/users')
    with app.app_context():
        db.create_all()
        if User.query.get(1) is None:
            user = User()
            data = {
              'login': 'kotlin',
               'email': 'ladonya.s@gmail.com',
              'first_name': 'Kotlin',
              'last_name': 'Jackson',
              'passwd': '1234567q',
              'avatar64': None
            }
            user.import_data(data)
            user.create_userfolder()
            db.session.add(user)
            db.session.commit()
        if Movie.query.get(1) is None:
            movies = []
            movies.append({
                'id': 1,
                'title': 'Movie 1',
                'year': 1968,
                'rating': 100500,
                'photo_url': 'http://localhost:5000/static/movies/movie_1/movie_1.png',
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
                'photo_url': 'http://localhost:5000/static/movies/movie_2/movie_2.png',
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
                'photo_url': 'http://localhost:5000/static/movies/movie_3/movie_3.png',
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
                'photo_url': 'http://localhost:5000/static/movies/movie_4/movie_4.jpg',
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
                'photo_url': 'http://localhost:5000/static/movies/movie_5/movie_5.png',
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
                'photo_url': 'http://localhost:5000/static/movies/movie_6/movie_6.jpg',
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
                'photo_url': 'http://localhost:5000/static/movies/movie_7/movie_7.jpg',
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
    app.run()
