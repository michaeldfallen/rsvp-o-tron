from flask_wtf import Form
from wtforms import TextField, validators


class AddGuestForm(Form):
    first_name = TextField('first_name', [validators.DataRequired()])
    last_name = TextField('last_name', [validators.DataRequired()])
