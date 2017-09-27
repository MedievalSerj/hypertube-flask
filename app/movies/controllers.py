from . import movies_blueprint
from .movie_model import Movie
from flask import jsonify, request


@movies_blueprint.route('/add', methods=['POST'])
def add_movie():
    movie = Movie()
    movie.import_data(request.json)
    db.session.add(movie)
    db.session.commit()
    return jsonify({}), 201, {'Location': movie.get_self_url()}


@movies_blueprint.route('/get_one/<int:id>')
def get_one(id):
    return jsonify(Movie.query.get_or_404(id).get_search_item())


@movies_blueprint.route('/search/<int:start>/<int:stop>')
def search(start, stop):
    all = [m.get_search_item() for m in Movie.query.all()]
    return jsonify({'search_results': all[start:stop]})


@movies_blueprint.route('/watch/<int:id>')
def watch(id):
    return jsonify(Movie.query.get_or_404(id).get_watch_item())
