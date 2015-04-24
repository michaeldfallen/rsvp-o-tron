from flask import redirect, url_for, session
from app.rsvp import views
from app.rsvp.model import RSVP
from app.invite.model import Invite
from app.rsvp.forms import FindInviteForm, AttendanceForm


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
            return redirect(url_for('rsvp.invite_details', token=invite.token))

    @blueprint.route('/rsvp/<string:token>/invite-details')
    def invite_details(token):
        form = AttendanceForm()
        invite = Invite.get(token)
        return views.Step2InviteDetails(invite, form).render()

    @blueprint.route('/rsvp/<string:token>/invite-details', methods=['POST'])
    def attendance(token):
        form = AttendanceForm()
        invite = Invite.get(token)
        if form.validate_on_submit():
            rsvp = form.bind()
            session['rsvp'] = rsvp.to_json()
            session.modified = True
            return redirect(url_for('rsvp.confirm', token=token))
        else:
            return views.Step2InviteDetails(invite, form).render()

    @blueprint.route('/rsvp/<string:token>/confirm')
    def confirm(token):
        return views.ConfirmStep().render()
