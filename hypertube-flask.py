#!/usr/bin/env python
import os
import datetime
from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy import PrimaryKeyConstraint
from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
from PIL import Image
from io import BytesIO
import base64
import uuid

from pprint import pprint
from sqlalchemy.engine import Engine
from sqlalchemy import event



basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data.sqlite')

app = Flask(__name__)
CORS(app)
app.config.update(dict(
    NG_ADDRESS='http://localhost:4200',
    ROOT_DIRECTORY=os.getcwd(),
    SQLALCHEMY_DATABASE_URI='sqlite:///' + db_path,
    UPLOAD_FOLDER='/nfs/2016/s/sladonia/repo/hypertube-flask/static/users',
    SECRET_KEY='wilhelm-marduk',
    DEBUG=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='ladonya.s@gmail.com',
    MAIL_PASSWORD=os.environ.get('G_PASSWD'),
))
db = SQLAlchemy(app)
mail = Mail(app)


class ValidationError(ValueError):
    pass


@app.errorhandler(ValidationError)
def bad_request(e):
    response = jsonify({
        'status': 400,
        'error': 'bad request',
        'message': e.args[0]
    })
    response.status_code = 400
    return response


@app.errorhandler(404)
def not_found(e):
    response = jsonify({
        'status': 404,
        'error': 'not found',
        'message': 'invalid URI'
    })
    response.status_code = 404
    return response


@app.errorhandler(405)
def method_not_supported(e):
    response = jsonify({
        'status': 405,
        'error': 'method not supported',
        'message': e.args[0]
    })
    response.status_code = 405
    return response


@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({
        'status': 500,
        'error': 'internal servererror',
        'message': e.args
    })
    response.status_code = 500
    return response


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


class WatchedMovie(db.Model):
    __tablename__ = 'watched_movies'
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    __table_args__ = (PrimaryKeyConstraint('movie_id', 'user_id', name='watched_movies_pk'),
                      {})
    
    def get_url(self):
        return url_for('get_watched_movies', user_id=self.user_id, _external=True)
    
    def export_data(self):
        return self.movie_id
    
    def import_data(self, data):
        try:
            self.movie_id = data['movie_id']
            self.user_id = data['user_id']
        except KeyError as e:
            raise ValidationError('Invalid WatchMovie: missing ' + e.args[0])


@app.route('/watched_movies', methods=['POST'])
def add_watched_movie():
    data = request.json
    watched_movie = WatchedMovie.query.filter_by(user_id=data['user_id'], movie_id=data['movie_id']).first()
    print('watched_movie = ' + str(watched_movie))
    if watched_movie is None:
        watched_movie = WatchedMovie()
        watched_movie.import_data(request.json)
        db.session.add(watched_movie)
        db.session.commit()
    return jsonify({}), 201


@app.route('/watched_movies/<int:user_id>', methods=['GET'])
def get_watched_movies(user_id):
    watched_movies = WatchedMovie.query.filter_by(user_id=user_id).all()
    result = [movie.export_data() for movie in watched_movies]
    pprint(result)
    return jsonify(result), 200


@app.route('/is_watched/<int:user_id>/<int:movie_id>', methods=['GET'])
def is_watched(user_id, movie_id):
    movie = WatchedMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if movie is None:
        msg = 'KO'
    else:
        msg = 'OK'
    return jsonify({"is_watched": msg}), 200


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
    

@app.route('/comments/<int:movie_id>', methods=['GET'])
def get_all_comments(movie_id):
    comments = Comment.query.filter_by(movie_id=movie_id).all()
    result = [comment.export_data() for comment in comments]
    return jsonify({"comments": result}), 200


@app.route('/comments', methods=['POST'])
def post_comment():
    comment = Comment()
    comment.import_data(request.json)
    db.session.add(comment)
    db.session.commit()
    return jsonify({}), 201


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    jwt = db.Column(db.String)
    avatar_url = db.Column(db.String(256))
    passwd = db.Column(db.String(256))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    registration_token = db.Column(db.String(128))
    activated = db.Column(db.Integer, default=0)
    join_date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    watched_movies = db.relationship('WatchedMovie', backref=db.backref('user', lazy='joined'), lazy='dynamic',
                                     cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref=db.backref('user', lazy='joined'), lazy='dynamic',
                               cascade='all, delete-orphan')
    
    def __init__(self):
        self.image_base64 = None
    
    def get_url(self):
        return url_for('get_user', user_id=self.user_id, _external=True)
    
    def export_data(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'join_date': self.join_date.isoformat() + 'Z',
            'watched_movies': url_for('get_watched_movies', user_id=self.user_id, _external=True)
        }
    
    def import_data(self, data):
        try:
            self.login = data['login']
            self.email = data['email']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.passwd = generate_password_hash(data['passwd'])
            self.image_base64 = data['avatar64']
            # print(data['avatar64'])
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        
    def modify_data(self, data):
        if 'login' in data:
            self.login = data['login']
        if 'email' in data:
            self.email = data['email']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'passwd' in data:
            self.passwd = data['passwd']
            
    def exists(self):
        login_exists = User.query.filter_by(login=self.login).first()
        email_exists = User.query.filter_by(email=self.email).first()
        if login_exists or email_exists:
            return True
        return False
    
    def create_userfolder(self):
        os.mkdir(app.config['ROOT_DIRECTORY'] + '/static/users/' + self.login)
    
    def save_img(self):
        if self.image_base64 is None:
            return
        im = Image.open(BytesIO(base64.b64decode(self.image_base64.split(',')[1])))
        im_filename = str(uuid.uuid4()) + '.' + im.format
        im_dbpath = '/static/' + self.login + '/' + im_filename
        im_filepath = os.path.join(app.config['ROOT_DIRECTORY'],
                                    'static', 'users', self.login, im_filename)
        im.save(im_filepath)
        self.avatar_url = im_dbpath
        
    def send_confirm_email(self):
        token = str(uuid.uuid4())
        subject = 'Hypertube email confirmation'
        sender = 'http://localhost:4200/'
        recipient = self.email
        body = '''Greetings new hypertube user!
        \n\nPlease follow the link to finish registration:
        \n{0}'''.format(app.config['NG_ADDRESS']
                        + '/sign-in/?confirmed=true&token=' +
                        token +
                        '&login=' +
                        self.login)
        msg = Message(sender=sender,
                      recipients=[recipient],
                      subject=subject,
                      body=body
                      )
        self.registration_token = token
        mail.send(msg)


@app.route('/confirm_email/<string:login>/<string:token>', methods=['GET'])
def confirm_email(login, token):
    user = User.query.filter_by(login=login, registration_token=token).first()
    if user is None:
        return jsonify({'confirmed': False}), 200
    user.activated = 1
    db.session.commit()
    return jsonify({'confirmed': True}), 200


@app.route('/user', methods=['POST'])
def add_user():
    user = User()
    user.import_data(request.json)
    if user.exists():
        return jsonify({'exists': True}), 200
    user.create_userfolder()
    user.save_img()
    db.session.add(user)
    user.send_confirm_email()
    db.session.commit()
    return jsonify({'exists': False}), 201, {'Location': user.get_url()}


@app.route('/user_exists/<string:login>', methods=['GET'])
def user_exists(login):
    exists = False
    user = User.query.filter_by(login=login).first()
    if user:
        exists = True
    return jsonify({'user_exists': exists})


@app.route('/email_exists/<string:email>', methods=['GET'])
def email_exists(email):
    exists = False
    user = User.query.filter_by(email=email).first()
    if user:
        exists = True
    return jsonify({'email_exists': exists})


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({})


@app.route('/user/<int:user_id>', methods=['PATCH'])
def modify_user(user_id):
    user = User.query.get_or_404(user_id)
    user.modify_data(request.json)
    db.session.commit()
    return jsonify({})
    

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.export_data())


# hook for sqlite foreign key restriction
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def authenticate(username, password):
    print('auth breakpoint')
    
    user = User.query.filter_by(login=username).first()
    if user is None:
        user = User.query.filter_by(email=username).first()
    if user and check_password_hash(user.passwd, password):
        print('auth breakpoint')
        return user
    return None


def identity(payload):
    print('identity breakpoint')
    
    return User.query.filter_by(user_id=payload['identity']).first()


jwt = JWT(app, authenticate, identity)


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected_function():
    return '%s' % current_identity.user_id


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
        except Exception as e:
            pass
    app.run(debug=True)
