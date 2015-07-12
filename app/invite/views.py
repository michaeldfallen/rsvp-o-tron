from app.views.template import Template
from app.forms import FormHandler


class CreateInvite(Template, FormHandler):

    def __init__(self, form):
        self.form = form

    def title(self):
        return "Create an Invite"


class ListInvites(Template):

    def __init__(self, invites=[]):
        def by_id(invite):
            return invite.id

        self.invites = sorted(list(invites), key=by_id, reverse=True)

    def title(self):
        return "All Invites"
