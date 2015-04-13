import unittest
from test.helpers import with_client, setUpApp
from test.helpers import with_context, setUpDB, tearDownDB
from lxml.html import document_fromstring


class TestRoutes(unittest.TestCase):

    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @with_context
    @with_client
    def test_start_route(self, client):
        res = client.get('/rsvp')
        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_find_invite(self, client):
        res = client.post('/rsvp', data={'token': 'shouldfail'})
        html = document_fromstring(res.get_data())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            html.xpath("//div[@class='error']/text()"),
            ["We couldn't find your invitation"]
        )
