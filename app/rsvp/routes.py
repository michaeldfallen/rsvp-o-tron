from app.rsvp import views
from app.rsvp.model import RSVP


def register_routes(blueprint):
    @blueprint.route('/rsvp')
    def start():
        return views.Step1Start().render()
