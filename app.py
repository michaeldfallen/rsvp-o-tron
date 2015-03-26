from flask import Flask, redirect, url_for
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
def list_invites():
    all_invites = Invite.all()
    return views.ListInvites(all_invites).render()


@app.route('/invite/new')
def create_invite_form():
    return views.CreateInvite().render()


@app.route('/invite/new', methods=['POST'])
def create_invite():
    invite = Invite()
    Invite.save(invite)
    return redirect(url_for('list_invites'))

if __name__ == '__main__':
    manager.run()
