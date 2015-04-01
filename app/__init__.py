# flake8: noqa
from flask import Flask
from flask.ext.script import Manager
from app import invite, guest

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(guest.blueprint)
app.register_blueprint(invite.blueprint)

manager = Manager(app)
db.init(app, manager)
