from flask import redirect, url_for
from app.invite import views
from app.invite.forms import CreateInviteForm
from app.invite.model import Invite


def register_routes(blueprint):
    @blueprint.route('/invite')
    def list_invites():
        all_invites = Invite.all()
        return views.ListInvites(all_invites).render()

    @blueprint.route('/invite/new')
    def create_invite_form():
        form = CreateInviteForm()
        return views.CreateInvite(form).render()

    @blueprint.route('/invite/new', methods=['POST'])
    def create_invite():
        form = CreateInviteForm()
        if form.validate_on_submit():
            invite = Invite(has_room=form.has_room.data)
            Invite.save(invite)
            return redirect(url_for('invite.list_invites'))
        else:
            return views.CreateInvite(form).render()

    @blueprint.route('/invite/<token>/delete', methods=['POST'])
    @blueprint.route('/invite/<token>', methods=['DELETE'])
    def delete_invite(token):
        Invite.delete(token)
        return redirect(url_for('invite.list_invites'))
