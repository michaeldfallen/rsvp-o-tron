import unittest
from test.helpers import with_context, setUpDB, setUpApp, tearDownDB
from app.guest.model import Guest
from app.invite.model import Invite


class TestModel(unittest.TestCase):

    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @with_context
    def test_get_guest(self):
        invite = Invite()
        invite.save()
        guest = Guest('Jim', 'Smith', invite.id)
        guest.save()

        self.assertEqual(guest, Guest.get(guest.id))
