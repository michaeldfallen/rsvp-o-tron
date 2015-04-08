from flask import Blueprint
from app.rsvp import routes


blueprint = Blueprint('rsvp', __name__)
routes.register_routes(blueprint)
