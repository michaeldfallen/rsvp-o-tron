from flask_wtf import Form
from wtforms import TextField, validators


class FindInviteForm(Form):
    token = TextField('token', [validators.DataRequired()])
