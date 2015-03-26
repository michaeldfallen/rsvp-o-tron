from flask import Flask
from flask.ext.script import Manager
import db
import views
from model import Invite

app = Flask(__name__)
app.config.from_pyfile('config.py')
manager = Manager(app)
db.init(app, manager)


@app.route('/')
def hello():
    return views.Home.render()


@app.route('/list-invites')
def listInvites():
    all_invites = Invite.all()
    return views.ListInvites(all_invites).render()


if __name__ == '__main__':
    manager.run()
