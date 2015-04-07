from flask import Flask
from flask.ext.script import Manager
from app import invite, guest, rsvp, db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.register_blueprint(guest.blueprint)
    app.register_blueprint(invite.blueprint)
    app.register_blueprint(rsvp.blueprint)

    manager = Manager(app)
    db.init(app, manager)
    return app, manager
