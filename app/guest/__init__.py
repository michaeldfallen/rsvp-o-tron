# flake8: noqa
from flask import Blueprint
from . import add_guest

blueprint = Blueprint('guest', __name__)
add_guest.routes(blueprint)
