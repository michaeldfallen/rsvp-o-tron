from app.views.template import Template
from app.model import Guest, Invite
from flask_wtf import Form
from wtforms import TextField, validators
from flask import redirect, url_for


class AddGuestForm(Form):
    first_name = TextField('first_name', [validators.DataRequired()])
    last_name = TextField('last_name', [validators.DataRequired()])


class AddGuest(Template):

    def __init__(self, invite_token, form):
        self.token = invite_token
        self.form = form

    def title(self):
        return "Add a guest"


def routes(blueprint):
    @blueprint.route('/invite/<token>/guest', methods=['POST'])
    def add_guest_to_invite(token):
        form = AddGuestForm()
        if form.validate_on_submit():
            invite = Invite.get(token)
            guest = Guest(
                form.first_name.data,
                form.last_name.data,
                invite.id
            )
            guest.save()
            return redirect(url_for('list_invites'))
        else:
            return AddGuest(token, form).render()

    @blueprint.route('/invite/<token>/guest/new', methods=['GET'])
    def add_guest_form(token):
        form = AddGuestForm()
        return AddGuest(token, form).render()
