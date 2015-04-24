import unittest
from test.helpers import with_context, setUpApp, TestForm
from lxml.html import document_fromstring
from app.rsvp.views import Step1Start, Step2InviteDetails
from app.invite.model import Invite
from app.guest.model import Guest


class TestViews(unittest.TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_step1_start(self):
        html = document_fromstring(Step1Start(TestForm()).render())
        self.assertEquals(
            html.xpath("//title/text()")[0],
            "Hello, Guest!"
        )

    @with_context
    def test_step2_invite_details(self):
        invite = Invite()
        invite.id = 123456789
        joe = Guest('Joe', 'Smith', invite.id)
        joe.id = 1
        jane = Guest('Jane', 'Smith', invite.id)
        jane.id = 2
        invite.guests = [joe, jane]

        page = Step2InviteDetails(invite, TestForm())

        html = document_fromstring(page.render())
        self.assertEqual(
            html.xpath('//li[@class="guest"]/text()'),
            ['Joe Smith', 'Jane Smith']
        )
