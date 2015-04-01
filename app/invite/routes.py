from flask import redirect, url_for
from app.invite import views
from app.invite.model import Invite


def register_routes(blueprint):
    @blueprint.route('/invite')
    def list_invites():
        all_invites = Invite.all()
        return views.ListInvites(all_invites).render()

    @blueprint.route('/invite/new')
    def create_invite_form():
        return views.CreateInvite().render()

    @blueprint.route('/invite/new', methods=['POST'])
    def create_invite():
        invite = Invite()
        Invite.save(invite)
        return redirect(url_for('list_invites'))

    @blueprint.route('/invite/<token>/delete', methods=['POST'])
    @blueprint.route('/invite/<token>', methods=['DELETE'])
    def delete_invite(token):
        Invite.delete(token)
        return redirect(url_for('list_invites'))
