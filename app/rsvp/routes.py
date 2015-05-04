from flask import redirect, url_for, session
from app.rsvp import views
from app.rsvp.model import RSVPSet
from app.invite.model import Invite
from app.guest.model import Guest
from app.rsvp.forms import FindInviteForm, AttendanceForm


def __continue_or_go_to_confirm(rsvpset, token):
    next_rsvp = rsvpset.next_rsvp()
    if next_rsvp is not None:
        return redirect(url_for('rsvp.attending',
                                token=token,
                                **rsvpset.next_rsvp()))
    else:
        return redirect(url_for('rsvp.confirm', token=token))


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
        return __continue_or_go_to_confirm(rsvpset, token)

    @blueprint.route('/rsvp/<token>/<int:guest_id>/<name>/attending')
    def attending(token, guest_id, name):
        form = AttendanceForm()
        guest = Guest.get(guest_id)
        return views.Step3Respond(form, guest).render()

    @blueprint.route('/rsvp/<token>/<int:guest_id>/<name>/attending',
                     methods=['POST'])
    def attending_post(token, guest_id, name):
        form = AttendanceForm()
        if form.validate_on_submit():
            rsvpset = RSVPSet.from_json(session['rsvp'])
            rsvpset.update_attending(guest_id, form.bind())
            session['rsvp'] = rsvpset.to_json()
            session.modified = True
            return __continue_or_go_to_confirm(rsvpset, token)
        else:
            guest = Guest.get(guest_id)
            return views.Step3Respond(form, guest).render()

    @blueprint.route('/rsvp/<string:token>/confirm')
    def confirm(token):
        rsvpset = RSVPSet.from_json(session['rsvp'])
        return views.ConfirmStep(rsvpset.rsvps).render()
