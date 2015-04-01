from app.views.template import Template


class CreateInvite(Template):

    def title(self):
        return "Create an Invite"


class ListInvites(Template):

    def __init__(self, invites=[]):
        self.invites = invites

    def title(self):
        return "All Invites"
