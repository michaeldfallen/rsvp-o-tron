from views.template import Template
from wtforms import Form, TextField, validators
from flask import redirect, url_for


class AddGuestForm(Form):
    first_name = TextField('first_name', [validators.Length(min=3)])
    last_name = TextField('last_name', [validators.Length(min=3)])


class AddGuest(Template):

    def __init__(self, invite_token):
        self.token = invite_token

    def title(self):
        return "Add a guest"


def routes(app):
    @app.route('/invite/<token>/guest', methods=['POST'])
    def add_guest_to_invite(token):
        return redirect(url_for('list_invites'))

    @app.route('/invite/<token>/guest/new', methods=['GET'])
    def add_guest_form(token):
        return AddGuest(token).render()
