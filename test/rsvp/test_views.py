import unittest
from test.helpers import with_context, setUpApp, TestForm
from lxml.html import document_fromstring
from app.rsvp.views import Step1Start, Step2InviteDetails, FinishedStep
from app.invite.model import Invite
from app.guest.model import Guest
from app.rsvp.model import RSVP


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

        page = Step2InviteDetails(invite)

        html = document_fromstring(page.render())
        self.assertEqual(
            html.xpath('//li[@class="guest"]/text()'),
            ['Joe Smith', 'Jane Smith']
        )

    @with_context
    def test_finished_step(self):
        invite = Invite()
        invite.id = 123456789
        joe = Guest('Joe', 'Smith', invite.id)
        joe.id = 1
        joe_rsvp = RSVP(joe.id, joe.first_name)
        joe_rsvp.guest = joe
        joe_rsvp.attending = True
        jane = Guest('Jane', 'Smith', invite.id)
        jane.id = 2
        jane_rsvp = RSVP(jane.id, jane.first_name)
        jane_rsvp.guest = jane
        jane_rsvp.attending = False
        invite.guests = [joe, jane]

        rsvps = [jane_rsvp, joe_rsvp]

        view = FinishedStep(rsvps)

        self.assertEqual([jane_rsvp], list(view.people_avoiding()))
        self.assertEqual([joe_rsvp], list(view.people_attending()))

        html = document_fromstring(view.render())
        self.assertIn('Joe',
                      html.xpath('//div[@class="attending"]//li/text()'))
        self.assertIn('Jane',
                      html.xpath('//div[@class="avoiding"]//li/text()'))
