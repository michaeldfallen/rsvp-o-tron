from flask import Blueprint
from . import routes


blueprint = Blueprint('invite', __name__)
routes.register_routes(blueprint)
