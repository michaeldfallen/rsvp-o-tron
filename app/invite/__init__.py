from flask import Blueprint
from . import routes


def blueprint(auth):
    blueprint_ = Blueprint('invite', __name__)
    routes.register_routes(blueprint_, auth)
    return blueprint_
