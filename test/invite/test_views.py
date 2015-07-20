import unittest
from app.invite.views import ListInvites
from app.invite.model import Invite
from app.guest.model import Guest
from app.rsvp.model import RSVP


class TestViews(unittest.TestCase):

    def test_no_invites(self):
        invites = []
        view = ListInvites(invites=invites)

        self.assertEqual(view.num_beef(), 0)
        self.assertEquals(view.num_turkey(), 0)
        self.assertEquals(view.num_vegetarian(), 0)
        self.assertEquals(view.num_not_responded(), 0)
        self.assertEquals(view.num_attending(), 0)
        self.assertEquals(view.num_attending(), 0)

    def test_attending_or_avoiding(self):
        invite1 = Invite()
        invite1.id = 1
        john = Guest('John', 'Smith', invite1.id)
        john.id = 3
        johns_rsvp = RSVP(john.id, john.first_name)
        john.rsvp = johns_rsvp
        invite1.guests = [john]
        invites = [invite1]

        view = ListInvites(invites=invites)

        self.assertEqual(view.num_not_responded(), 1)
        self.assertEqual(view.num_attending(), 0)
        self.assertEqual(view.num_avoiding(), 0)

        johns_rsvp.attending = True

        self.assertEqual(view.num_not_responded(), 0)
        self.assertEqual(view.num_attending(), 1)
        self.assertEqual(view.num_avoiding(), 0)

        johns_rsvp.attending = False

        self.assertEqual(view.num_not_responded(), 0)
        self.assertEqual(view.num_attending(), 0)
        self.assertEqual(view.num_avoiding(), 1)

    def test_menu_choices(self):
        invite1 = Invite()
        invite1.id = 1
        john = Guest('John', 'Smith', invite1.id)
        john.id = 3
        johns_rsvp = RSVP(john.id, john.first_name)
        john.rsvp = johns_rsvp
        invite1.guests = [john]
        invites = [invite1]

        view = ListInvites(invites=invites)

        self.assertEqual(view.num_beef(), 0)
        self.assertEqual(view.num_turkey(), 0)
        self.assertEqual(view.num_vegetarian(), 0)

        johns_rsvp.menu_choice = 'beef'

        self.assertEqual(view.num_beef(), 1)
        self.assertEqual(view.num_turkey(), 0)
        self.assertEqual(view.num_vegetarian(), 0)

        johns_rsvp.menu_choice = 'turkey'

        self.assertEqual(view.num_beef(), 0)
        self.assertEqual(view.num_turkey(), 1)
        self.assertEqual(view.num_vegetarian(), 0)

        johns_rsvp.menu_choice = 'vegetarian'

        self.assertEqual(view.num_beef(), 0)
        self.assertEqual(view.num_turkey(), 0)
        self.assertEqual(view.num_vegetarian(), 1)
