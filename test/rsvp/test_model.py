import unittest
from test.helpers import with_context, setUpDB, setUpApp, tearDownDB
from app.rsvp.model import RSVP
from app.guest.model import Guest
from app.invite.model import Invite
from sqlalchemy.exc import IntegrityError


class TestModel(unittest.TestCase):

    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @staticmethod
    def make_guest():
        invite = Invite()
        invite.save()

        guest = Guest('John', 'Smith', invite.id)
        guest.save()
        return guest

    @with_context
    def test_insert_fails_with_no_attendance(self):
        rsvp = RSVP(self.make_guest().id)
        with self.assertRaises(IntegrityError):
            rsvp.save()

    @with_context
    def test_insert(self):
        rsvp = RSVP(self.make_guest().id)
        rsvp.attending = True
        rsvp.save()
        savedrsvp = RSVP.get(rsvp.id)
        self.assertEquals(rsvp, savedrsvp)

    @with_context
    def test_relationship_to_guest(self):
        guest = self.make_guest()
        rsvp = RSVP(guest.id)
        rsvp.attending = True
        rsvp.save()

        savedrsvp = RSVP.get(rsvp.id)
        self.assertEquals(
            savedrsvp.guest_id,
            rsvp.guest_id
        )
        self.assertEquals(
            savedrsvp.guest,
            rsvp.guest
        )
