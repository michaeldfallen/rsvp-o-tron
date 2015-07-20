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
        self.rsvps = [
            guest.rsvp
            for invite in invites
            for guest in invite.guests
        ]

    def title(self):
        return "All Invites"

    def count(self, predicate):
        def _1_if_predicate_passes(rsvp):
            return 1 if predicate(rsvp) else 0

        totals = map(_1_if_predicate_passes, self.rsvps)
        return sum(totals)

    def num_attending(self):
        def _is_attending(rsvp):
            return rsvp is not None and rsvp.attending is True

        return self.count(_is_attending)

    def num_avoiding(self):
        def _is_avoiding(rsvp):
            return rsvp is not None and rsvp.attending is False

        return self.count(_is_avoiding)

    def num_not_responded(self):
        def _not_responded(rsvp):
            return rsvp is None or rsvp.attending is None

        return self.count(_not_responded)

    def num_beef(self):
        def _beef(rsvp):
            return (rsvp is not None and
                    rsvp.menu_choice is not None and
                    rsvp.menu_choice == 'beef')

        return self.count(_beef)

    def num_turkey(self):
        def _turkey(rsvp):
            return (rsvp is not None and
                    rsvp.menu_choice is not None and
                    rsvp.menu_choice == 'turkey')

        return self.count(_turkey)

    def num_vegetarian(self):
        def _vegetarian(rsvp):
            return (rsvp is not None and
                    rsvp.menu_choice is not None and
                    rsvp.menu_choice == 'vegetarian')

        return self.count(_vegetarian)
