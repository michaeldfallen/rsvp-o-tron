from views.template import Template


class AddGuest(Template):

    def __init__(self, invite_token):
        self.token = invite_token

    def title(self):
        return "Add a guest"
