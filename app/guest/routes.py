from app.guest.model import Guest
from app.invite.model import Invite
from app.guest import views
from app.guest.forms import AddGuestForm
from flask import redirect, url_for


def register_routes(blueprint):
    @blueprint.route('/invite/<token>/guest', methods=['POST'])
    def add_guest_to_invite(token):
        form = AddGuestForm()
        if form.validate_on_submit():
            invite = Invite.get(token)
            guest = Guest(
                form.first_name.data,
                form.last_name.data,
                invite.id
            )
            guest.save()
            return redirect(url_for('list_invites'))
        else:
            return views.AddGuest(token, form).render()

    @blueprint.route('/invite/<token>/guest/new', methods=['GET'])
    def add_guest_form(token):
        form = AddGuestForm()
        return views.AddGuest(token, form).render()

    @blueprint.route('/invite/<token>/guest/<id>/delete', methods=['POST'])
    @blueprint.route('/invite/<token>/guest/<id>', methods=['DELETE'])
    def delete_guest(token, id):
        Guest.delete(id)
        return redirect(url_for('list_invites'))
