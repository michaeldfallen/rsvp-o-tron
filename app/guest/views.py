from app.views.template import Template


class AddGuest(Template):

    def __init__(self, invite_token, form):
        self.token = invite_token
        self.form = form

    def title(self):
        return "Add a guest"
