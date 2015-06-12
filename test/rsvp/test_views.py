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
        self.assertTrue(view.are_people_avoiding())
        self.assertEqual([joe_rsvp], list(view.people_attending()))
        self.assertTrue(view.are_people_attending())

        html = document_fromstring(view.render())
        self.assertIn('Joe',
                      html.xpath('//div[@class="attending"]//li/text()'))
        self.assertIn('Jane',
                      html.xpath('//div[@class="avoiding"]//li/text()'))

        jane_rsvp.attending = False
        joe_rsvp.attending = False

        view = FinishedStep(rsvps)

        self.assertEqual([jane_rsvp, joe_rsvp], list(view.people_avoiding()))
        self.assertTrue(view.are_people_avoiding())
        self.assertEqual([], list(view.people_attending()))
        self.assertFalse(view.are_people_attending())

        jane_rsvp.attending = True
        joe_rsvp.attending = True

        view = FinishedStep(rsvps)

        self.assertEqual([], list(view.people_avoiding()))
        self.assertFalse(view.are_people_avoiding())
        self.assertEqual([jane_rsvp, joe_rsvp], list(view.people_attending()))
        self.assertTrue(view.are_people_attending())

    def test_readable_menu_choices(self):
        john = RSVP(1234, "John")
        john.attending = True
        john.menu_choice = "turkey"

        george = RSVP(1231, "George")
        george.attending = False

        ringo = RSVP(1232, "Ringo")
        ringo.attending = True
        ringo.menu_choice = "beef"

        paul = RSVP(1233, "Paul")
        paul.attending = True
        paul.menu_choice = "vegetarian"

        rsvps = [john, paul, george, ringo]

        expected = [
            {
                "name": "John",
                "choice": "the Turkey and Ham"
            },
            {
                "name": "Paul",
                "choice": "the tarte tatin"
            },
            {
                "name": "Ringo",
                "choice": "the Roast sirloin of Beef"
            }
        ]
        self.assertEqual(expected, FinishedStep(rsvps).menu_choices())
