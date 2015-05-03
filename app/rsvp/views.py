from app.views.template import Template
from app.forms import FormHandler


class Step1Start(Template, FormHandler):
    title = "Hello, Guest!"

    def __init__(self, form):
        self.form = form


class Step2InviteDetails(Template):
    title = "Please join us at our wedding"

    def __init__(self, invite):
        self.invite = invite


class Step3Respond(Template):
    title = "Will you attend?"


class ConfirmStep(Template):
    title = "Confirm your RSVP"

    def __init__(self, rsvp):
        self.rsvp = rsvp
