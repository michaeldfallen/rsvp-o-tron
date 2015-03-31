# flake8: noqa
from .add_guest import routes as add_guest_routes

def routes(app):
    add_guest_routes(app)
