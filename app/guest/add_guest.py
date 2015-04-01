from app.views.template import Template
from flask_wtf import Form
from wtforms import TextField, validators


class AddGuestForm(Form):
    first_name = TextField('first_name', [validators.DataRequired()])
    last_name = TextField('last_name', [validators.DataRequired()])


class AddGuest(Template):

    def __init__(self, invite_token, form):
        self.token = invite_token
        self.form = form

    def title(self):
        return "Add a guest"
