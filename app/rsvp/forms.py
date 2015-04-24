from flask_wtf import Form
from wtforms import TextField, SelectField, validators
from app.rsvp.model import RSVP


class FindInviteForm(Form):
    token = TextField('token', [validators.DataRequired()])


class AttendanceForm(Form):
    guest_id = TextField('guest-id', [validators.DataRequired()])
    attending = SelectField(
        'attending',
        [validators.DataRequired()],
        choices=[('true', 'False'), ('false', 'False')]
    )

    def bind(self):
        rsvp = RSVP(int(self.guest_id.data))
        rsvp.attending = bool(self.attending.data)
        return rsvp
