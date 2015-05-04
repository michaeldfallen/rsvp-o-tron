from flask import redirect, url_for, session
from app.rsvp import views
from app.rsvp.model import RSVPSet
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
        invite = Invite.get(token)
        return views.Step2InviteDetails(invite).render()

    @blueprint.route('/rsvp/<string:token>/invite-details', methods=['POST'])
    def invite_details_post(token):
        invite = Invite.get(token)
        rsvpset = RSVPSet(invite.id, invite.guests)
        session['rsvp'] = rsvpset.to_json()
        session.modified = True
        return redirect(url_for('rsvp.attending',
                                token=token,
                                **rsvpset.next_rsvp()))

    @blueprint.route('/rsvp/<token>/<int:guest_id>/<name>/attending')
    def attending(token, guest_id, name):
        return views.Step3Respond().render()

    @blueprint.route('/rsvp/<string:token>/respond', methods=['POST'])
    def respond_post(token):
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
        rsvp = RSVPSet.from_json(session['rsvp'])
        return views.ConfirmStep(rsvp).render()
