from app.rsvp import views


def register_routes(blueprint):
    @blueprint.route('/rsvp')
    def start():
        return views.Step1Start().render()
