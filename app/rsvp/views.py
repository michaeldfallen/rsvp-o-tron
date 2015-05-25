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


class Step3Respond(Template, FormHandler):
    title = "Will you attend?"

    def __init__(self, form, guest):
        self.guest = guest
        self.form = form


class ConfirmStep(Template):
    title = "Confirm your RSVP"

    def __init__(self, rsvps):
        self.rsvps = rsvps


class FinishedStep(Template):
    title = "Thanks for RSVPing"

    def __init__(self, rsvps):
        self.rsvps = rsvps

    def people_attending(self):
        def are_attending(o):
            return o.attending

        return filter(are_attending, self.rsvps)

    def are_people_attending(self):
        return len(list(self.people_attending())) != 0

    def people_avoiding(self):
        def are_not_attending(o):
            return not o.attending

        return filter(are_not_attending, self.rsvps)

    def are_people_avoiding(self):
        return len(list(self.people_avoiding())) != 0
