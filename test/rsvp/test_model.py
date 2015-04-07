import unittest
from test.dbtestcase import with_context, setUpDB, setUpApp, tearDownDB
from app.rsvp.model import RSVP
import sqlalchemy


class TestModel(unittest.TestCase):

    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @with_context
    def test_insert_fails_with_no_attendance(self):
        rsvp = RSVP()
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            rsvp.save()

    @with_context
    def test_insert(self):
        rsvp = RSVP()
        rsvp.attending = True
        rsvp.save()
        savedrsvp = RSVP.get(rsvp.id)
        self.assertEquals(rsvp, savedrsvp)
