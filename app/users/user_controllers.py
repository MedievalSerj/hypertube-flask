from flask import jsonify, request, abort, g
from . import users_blueprint
from .user_model import User
from .comment_model import Comment
from .watched_movie_model import WatchedMovie
from app import db
from werkzeug.security import check_password_hash
import jwt
from functools import wraps
from time import sleep

# from urllib import request, parse

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorisation')
        try:
            g.user_data = User.decode_token(token)
        except jwt.exceptions.DecodeError:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@users_blueprint.route('/oauth42/<string:code>', methods=['GET'])
def oauth42(code):
    sleep(0.1)
    print('code: ' + code)
    # data = {
    #     'grant_type': 'authorization_code',
    #     'client_id': '135caaea196569df717378f2950cfb4833e1a936d8c3c4a5f56f57fbec6935a4',
    #     'client_secret': 'b26e81d39a962c5304b0f8642cf670eab074893794faa08285a92d3e7eaebdad',
    #     'code': code,
    # }
    # encoded_data = parse.urlencode(data).encode()
    # req = request.Request('https://api.intra.42.fr/oauth/token', data=encoded_data)
    # resp = request.urlopen(req)
    # print('resp' + str(resp))
    return jsonify({'status': 'OK'}), 200


@users_blueprint.route('/reset', methods=['POST'])
def reset_email():
    data = request.json
    if 'email' not in data:
        abort(400)
    User.send_reset_email(data['email'])
    return jsonify({}), 200
    

@users_blueprint.route('/auth', methods=['POST'])
def auth():
    data = request.json
    if 'login' and 'passwd' not in data:
        abort(400)
    user = User.query.filter_by(login=data['login']).first()
    if user is None:
        abort(400)
    if not check_password_hash(user.passwd, data['passwd']):
        abort(400)
    token = user.get_token()
    return jsonify({'token': token}), 200


@users_blueprint.route('/confirm_email/<string:login>/<string:token>', methods=['GET'])
def confirm_email(login, token):
    user = User.query.filter_by(login=login, registration_token=token).first()
    if user is None:
        return jsonify({'confirmed': False}), 200
    user.activated = 1
    db.session.commit()
    return jsonify({'confirmed': True}), 200


@users_blueprint.route('/user', methods=['POST'])
def add_user():
    user = User()
    user.import_data(request.json)
    if user.exists():
        abort(409)
    user.save_img()
    db.session.add(user)
    user.send_confirm_email()
    db.session.commit()
    try:
        user.create_userfolder()
    except FileExistsError:
        abort(409)
    return jsonify({'exists': False}), 201, {'Location': user.get_url()}


@users_blueprint.route('/user_exists/<string:login>', methods=['GET'])
def user_exists(login):
    exists = False
    user = User.query.filter_by(login=login).first()
    if user:
        exists = True
    return jsonify({'user_exists': exists})


@users_blueprint.route('/email_exists/<string:email>', methods=['GET'])
def email_exists(email):
    exists = False
    user = User.query.filter_by(email=email).first()
    if user:
        exists = True
    return jsonify({'email_exists': exists})


@users_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user.remove_userfolder()
    db.session.delete(user)
    db.session.commit()
    return jsonify({})


@users_blueprint.route('/user/<int:user_id>', methods=['PATCH'])
def modify_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    #
    # print(data)
    #
    user.modify_data(data)
    db.session.commit()
    token = user.get_token()
    return jsonify({'token': token})


@users_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.export_data())


# COMMENT ROUTES


@users_blueprint.route('/comments/<int:movie_id>', methods=['GET'])
def get_all_comments(movie_id):
    comments = Comment.query.filter_by(movie_id=movie_id).all()
    result = [comment.export_data() for comment in comments]
    return jsonify({"comments": result}), 200


@users_blueprint.route('/comments', methods=['POST'])
def post_comment():
    comment = Comment()
    comment.import_data(request.json)
    db.session.add(comment)
    db.session.commit()
    return jsonify({}), 201


# WATCHED MOVIES ROUTES


@users_blueprint.route('/watched_movies', methods=['POST'])
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


@users_blueprint.route('/watched_movies/<int:user_id>', methods=['GET'])
def get_watched_movies(user_id):
    watched_movies = WatchedMovie.query.filter_by(user_id=user_id).all()
    result = [movie.export_data() for movie in watched_movies]
    return jsonify(result), 200


@users_blueprint.route('/is_watched/<int:user_id>/<int:movie_id>', methods=['GET'])
def is_watched(user_id, movie_id):
    movie = WatchedMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if movie is None:
        msg = 'KO'
    else:
        msg = 'OK'
    return jsonify({"is_watched": msg}), 200