import unittest
from test.helpers import with_context, setUpDB, setUpApp, tearDownDB
from app.invite.model import Invite
from app.guest.model import Guest
from app.rsvp.model import RSVP


class TestModel(unittest.TestCase):

    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @with_context
    def test_insert(self):
        invite = Invite()
        invite.save()
        savedinvite = Invite.get(invite.token)
        self.assertEqual(invite.id, savedinvite.id)

    def test_uuids_are_unique(self):
        invite1 = Invite()
        invite2 = Invite()
        self.assertNotEqual(invite1.token, invite2.token)

    @with_context
    def test_invite_is_complete(self):
        invite = Invite()
        invite.save()

        self.assertFalse(invite.is_complete())

        guest = Guest('John', 'Smith', invite.id)
        guest.save()
        invite.guests = [guest]

        self.assertFalse(invite.is_complete())

        rsvp = RSVP(guest.id, guest.first_name)
        rsvp.attending = True
        rsvp.menu_choice = 'beef'
        guest.rsvp = rsvp

        self.assertTrue(invite.is_complete())

        rsvp.attending = None
        self.assertFalse(invite.is_complete())
