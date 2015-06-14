from flask_wtf import Form
from wtforms import BooleanField


class CreateInviteForm(Form):
    has_room = BooleanField('has_room')
