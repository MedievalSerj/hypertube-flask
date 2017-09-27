from flask import jsonify, request
from . import users_blueprint
from .user_model import User
from .comment_model import Comment
from .watched_movie_model import WatchedMovie


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
        return jsonify({'exists': True}), 200
    user.create_userfolder()
    user.save_img()
    db.session.add(user)
    user.send_confirm_email()
    db.session.commit()
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
    db.session.delete(user)
    db.session.commit()
    return jsonify({})


@users_blueprint.route('/user/<int:user_id>', methods=['PATCH'])
def modify_user(user_id):
    user = User.query.get_or_404(user_id)
    user.modify_data(request.json)
    db.session.commit()
    return jsonify({})


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
    pprint(result)
    return jsonify(result), 200


@users_blueprint.route('/is_watched/<int:user_id>/<int:movie_id>', methods=['GET'])
def is_watched(user_id, movie_id):
    movie = WatchedMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if movie is None:
        msg = 'KO'
    else:
        msg = 'OK'
    return jsonify({"is_watched": msg}), 200