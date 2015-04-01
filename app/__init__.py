# flake8: noqa
from flask import Flask
from flask.ext.script import Manager
from app import routes, guest

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(guest.blueprint)

manager = Manager(app)
db.init(app, manager)
routes.routes(app)
