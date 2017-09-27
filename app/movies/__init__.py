from flask import Blueprint

movies_blueprint = Blueprint('controllers', __name__)

from . import controllers
