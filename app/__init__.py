from flask import Flask
from flask.ext.script import Manager
from app import invite, guest, rsvp, db
from app.auth import auth


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.register_blueprint(guest.blueprint)
    app.register_blueprint(invite.blueprint(auth))
    app.register_blueprint(rsvp.blueprint)

    manager = Manager(app)
    db.init(app, manager)
    return manager
