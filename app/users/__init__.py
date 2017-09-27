from flask import Blueprint

users_blueprint = Blueprint('controllers', __name__)

from . import controllers
