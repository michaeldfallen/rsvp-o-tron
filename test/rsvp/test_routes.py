import unittest
from test.helpers import with_client, setUpApp


class TestRoutes(unittest.TestCase):

    def setUp(self):
        setUpApp(self)

    @with_client
    def test_start_route(self, client):
        res = client.get('/rsvp')
        self.assertEqual(res.status_code, 200)
