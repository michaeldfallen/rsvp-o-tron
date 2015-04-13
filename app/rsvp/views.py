from app.views.template import Template
from app.forms import FormHandler


class Step1Start(Template, FormHandler):
    title = "Hello, Guest!"

    def __init__(self, form):
        self.form = form


class Step2InviteDetails(Template):
    title = "Please join us at our wedding"

    def __init__(self, form):
        self.form = form

    def errors(self):
        return self.form.errors
