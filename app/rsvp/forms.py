from flask_wtf import Form
from wtforms import TextField, SelectField, validators


class FindInviteForm(Form):
    token = TextField('token', [validators.DataRequired()])


class AttendanceForm(Form):
    attending = SelectField(
        'attending',
        [validators.DataRequired()],
        choices=[('true', 'True'), ('false', 'False')]
    )

    def bind(self):
        return self.attending.data in ['True', 'true']
