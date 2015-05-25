import unittest
from test.helpers import with_context, setUpDB, setUpApp, tearDownDB
from app.rsvp.model import RSVP, RSVPSet
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
        return guest, invite

    @with_context
    def test_insert_fails_with_no_attendance(self):
        guest, invite = self.make_guest()
        rsvp = RSVP(guest.id, guest.first_name)
        with self.assertRaises(IntegrityError):
            rsvp.save()

    @with_context
    def test_insert(self):
        guest, invite = self.make_guest()
        rsvp = RSVP(guest.id, guest.first_name)
        rsvp.attending = True
        rsvp.save()
        savedrsvp = RSVP.get(rsvp.id)
        self.assertEquals(rsvp, savedrsvp)

    @with_context
    def test_relationship_to_guest(self):
        guest, invite = self.make_guest()
        rsvp = RSVP(guest.id, guest.first_name)
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

    @with_context
    def test_rsvp_to_from_json(self):
        guest, invite = self.make_guest()

        rsvp = RSVP(guest.id, guest.first_name)
        json = rsvp.to_json()
        recovered = RSVP.from_json(json)

        self.assertEqual(rsvp, recovered)

        rsvp = RSVP(guest.id, guest.first_name)
        rsvp.attending = True
        rsvp.save()
        json = rsvp.to_json()
        recovered = RSVP.from_json(json)

        self.assertEqual(rsvp, recovered)

        rsvp = RSVP(guest.id, guest.first_name)
        rsvp.attending = True
        rsvp.save()
        json = rsvp.to_json()
        recovered = RSVP.from_json(json)

        self.assertEqual(rsvp, recovered)

    @with_context
    def test_rsvpset_to_from_json(self):
        guest, invite = self.make_guest()

        rsvpset = RSVPSet(invite.id, invite.guests)

        json = rsvpset.to_json()
        recovered = RSVPSet.from_json(json)

        self.assertEqual(rsvpset, recovered)
