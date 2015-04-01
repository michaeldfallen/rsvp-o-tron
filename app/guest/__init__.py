# flake8: noqa
from flask import Blueprint
from . import routes

blueprint = Blueprint('guest', __name__)
routes.register_routes(blueprint)
