from app.views.template import Template
from app.forms import FormHandler


class AddGuest(Template, FormHandler):

    def __init__(self, invite_token, form):
        self.token = invite_token
        self.form = form

    def title(self):
        return "Add a guest"
