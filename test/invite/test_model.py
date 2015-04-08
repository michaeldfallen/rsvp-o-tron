import unittest
from test.helpers import with_context, setUpDB, setUpApp, tearDownDB
from app.invite.model import Invite


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
