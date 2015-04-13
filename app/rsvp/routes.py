from app.rsvp import views
from app.rsvp.model import RSVP
from app.invite.model import Invite
from app.rsvp.forms import FindInviteForm


def register_routes(blueprint):
    @blueprint.route('/rsvp')
    def start():
        form = FindInviteForm()
        return views.Step1Start(form).render()

    @blueprint.route('/rsvp', methods=['POST'])
    def find_invite():
        form = FindInviteForm()
        invite = Invite.get(form.token.data)
        if invite is None:
            form.errors["global"] = ["We couldn't find your invitation"]
            return views.Step1Start(form).render()
        else:
            return views.Step2InviteDetails(form).render()
