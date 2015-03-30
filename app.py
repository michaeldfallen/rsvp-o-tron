from flask import Flask, redirect, url_for
from flask.ext.script import Manager
import db
import views
import add_guest
from model import Invite, Guest

app = Flask(__name__)
app.config.from_pyfile('config.py')
manager = Manager(app)
db.init(app, manager)
add_guest.routes(app)


@app.route('/')
def hello():
    return views.Home().render()


@app.route('/invite')
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


@app.route('/invite/<token>/delete', methods=['POST'])
@app.route('/invite/<token>', methods=['DELETE'])
def delete_invite(token):
    Invite.delete(token)
    return redirect(url_for('list_invites'))


@app.route('/invite/<token>/guest/<id>/delete', methods=['POST'])
@app.route('/invite/<token>/guest/<id>', methods=['DELETE'])
def delete_guest(token, id):
    Guest.delete(id)
    return redirect(url_for('list_invites'))


if __name__ == '__main__':
    manager.run()
