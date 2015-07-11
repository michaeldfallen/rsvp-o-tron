from flask import redirect, url_for, session
from app.rsvp import views
from app.rsvp.model import RSVPSet
from app.invite.model import Invite
from app.guest.model import Guest
from app.rsvp.forms import FindInviteForm, AttendanceForm, MenuOptionForm


def __continue_or_go_to_confirm(rsvpset, token):
    next_rsvp = rsvpset.next_rsvp()
    if next_rsvp is not None:
        return redirect(url_for('rsvp.attending',
                                token=token,
                                **rsvpset.next_rsvp()))
    else:
        rsvpset.save_responses()
        return redirect(url_for('rsvp.finished', token=token))


def __menu_choice_or_continue(current_rsvp, rsvpset, token):
    if current_rsvp.incomplete():
        return redirect(url_for(
            'rsvp.menu_choice',
            token=token,
            name=current_rsvp.name.lower(),
            guest_id=current_rsvp.guest_id
        ))
    else:
        return __continue_or_go_to_confirm(rsvpset, token)


def register_routes(blueprint):
    @blueprint.route('/')
    def start():
        form = FindInviteForm()
        return views.Step1Start(form).render()

    @blueprint.route('/', methods=['POST'])
    def find_invite():
        form = FindInviteForm()
        invite = Invite.get(form.token.data)
        if invite is None:
            form.errors["global"] = ["We couldn't find your invitation"]
            return views.Step1Start(form).render()
        elif invite.is_complete():
            return redirect(url_for('rsvp.already_finished',
                            token=invite.token))
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
            return __menu_choice_or_continue(
                rsvpset.rsvp_for(guest_id),
                rsvpset,
                token
            )
        else:
            guest = Guest.get(guest_id)
            return views.Step3Respond(form, guest).render()

    @blueprint.route('/rsvp/<token>/<int:guest_id>/<name>/menu-choice')
    def menu_choice(token, guest_id, name):
        form = MenuOptionForm()
        guest = Guest.get(guest_id)
        return views.Step4MenuChoices(form, guest).render()

    @blueprint.route('/rsvp/<token>/<int:guest_id>/<name>/menu-choice',
                     methods=['POST'])
    def menu_choice_post(token, guest_id, name):
        form = MenuOptionForm()
        if form.validate_on_submit():
            rsvpset = RSVPSet.from_json(session['rsvp'])
            rsvpset.update_menu_choice(guest_id, form.bind())
            session['rsvp'] = rsvpset.to_json()
            session.modified = True
            return __continue_or_go_to_confirm(rsvpset, token)
        else:
            guest = Guest.get(guest_id)
            return views.Step4MenuChoices(form, guest).render()

    @blueprint.route('/rsvp/<string:token>/confirm')
    def confirm(token):
        rsvpset = RSVPSet.from_json(session['rsvp'])
        return views.ConfirmStep(rsvpset.rsvps).render()

    @blueprint.route('/rsvp/<token>')
    def already_finished(token):
        invite = Invite.get(token)
        if invite is None:
            return redirect(url_for('rsvp.start'))
        else:
            rsvps = [guest.rsvp for guest in invite.guests]
            return views.FinishedStep(
                rsvps,
                already_finished=True,
                has_room=invite.has_room
            ).render()

    @blueprint.route('/rsvp/<token>/finished')
    def finished(token):
        invite = Invite.get(token)
        rsvps = [guest.rsvp for guest in invite.guests]
        return views.FinishedStep(rsvps, has_room=invite.has_room).render()
