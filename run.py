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
            user.activated = 1
            db.session.add(user)
            db.session.commit()
            user.create_userfolder()
        if Movie.query.get(1) is None:
            movies = []
            movies.append({
                'id': 1,
                'title': 'Перестрелка',
                'year': 1968,
                'rating': 7,
                'photo_url': 'http://localhost:5000/static/movies/movie_1/movie_1.png',
                'genre': 'Drama',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'description': 'story about an old fucked-up man and his dog...',
                'magnet_720': '37A523D93E34DA6897D80710A5764268E19A8A8F',
                'magnet_1080': '37A523D93E34DA6897D80710A5764268E19A8A8F'
            })
            movies.append({
                'id': 34,
                'title': 'Big Lebovski',
                'year': 2008,
                'rating': 6,
                'photo_url': 'http://localhost:5000/static/movies/movie_2/movie_2.png',
                'genre': 'Comedy',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'description': 'story about an old fucked-up man and his dog...',
                'magnet_720': '37A523D93E34DA6897D80710A5764268E19A8A8F',
                'magnet_1080': '37A523D93E34DA6897D80710A5764268E19A8A8F'
            })
            movies.append({
                'id': 21,
                'title': 'Матрица Времени',
                'year': 2017,
                'rating': 5,
                'photo_url': 'http://localhost:5000/static/movies/movie_3/movie_3.png',
                'genre': 'Thriller',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'description': 'story about an old fucked-up man and his dog...',
                'magnet_720': '37A523D93E34DA6897D80710A5764268E19A8A8F',
                'magnet_1080': '37A523D93E34DA6897D80710A5764268E19A8A8F'
            })
            movies.append({
                'id': 67,
                'title': 'Green Gold',
                'year': 2013,
                'rating': 8,
                'photo_url': 'http://localhost:5000/static/movies/movie_4/movie_4.jpg',
                'genre': 'Drama, Documentary',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'description': 'story about an old fucked-up man and his dog...',
                'magnet_720': '37A523D93E34DA6897D80710A5764268E19A8A8F',
                'magnet_1080': '37A523D93E34DA6897D80710A5764268E19A8A8F'
            })
            movies.append({
                'id': 42,
                'title': 'All girls weekend',
                'year': 2016,
                'rating': 3,
                'photo_url': 'http://localhost:5000/static/movies/movie_5/movie_5.png',
                'genre': 'Historical',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'description': 'story about an old fucked-up man and his dog...',
                'magnet_720': '37A523D93E34DA6897D80710A5764268E19A8A8F',
                'magnet_1080': '37A523D93E34DA6897D80710A5764268E19A8A8F'
            })
            movies.append({
                'id': 98,
                'title': 'Kill Switch',
                'year': 2001,
                'rating': 5,
                'photo_url': 'http://localhost:5000/static/movies/movie_6/movie_6.jpg',
                'genre': 'Action',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'description': 'story about an old fucked-up man and his dog...',
                'magnet_720': '37A523D93E34DA6897D80710A5764268E19A8A8F',
                'magnet_1080': '37A523D93E34DA6897D80710A5764268E19A8A8F'
            })
            movies.append({
                'id': 71,
                'title': 'La REINA DE ESPANA',
                'year': 1999,
                'rating': 4,
                'photo_url': 'http://localhost:5000/static/movies/movie_7/movie_7.jpg',
                'genre': 'Drama',
                'director': 'Big Boss',
                'actors': 'Robin Wiliams, Robin Good',
                'description': 'story about an old fucked-up man and his dog...',
                'magnet_720': '37A523D93E34DA6897D80710A5764268E19A8A8F',
                'magnet_1080': '37A523D93E34DA6897D80710A5764268E19A8A8F'
            })
            for movie in movies:
                movie_object = Movie()
                movie_object.import_data(movie)
                db.session.add(movie_object)
                db.session.commit()
    app.run(threaded=True)
