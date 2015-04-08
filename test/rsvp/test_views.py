import unittest
from test.viewtestcase import with_context, setUpApp
from lxml.html import document_fromstring
from app.rsvp.views import Step1Start


class TestViews(unittest.TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_step1_start(self):
        html = document_fromstring(Step1Start().render())
        self.assertEquals(
            html.xpath("//title/text()")[0],
            "Hello, Guest!"
        )
