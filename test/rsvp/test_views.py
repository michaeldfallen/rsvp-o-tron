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
    def test_step2_guest_names(self):
        invite = Invite()
        invite.id = 123456789
        joe = Guest('Joe', 'Smith', invite.id)
        joe.id = 1
        jane = Guest('Jane', 'Smith', invite.id)
        jane.id = 2
        jim = Guest('Jim', 'Smith', invite.id)
        jim.id = 3
        john = Guest('John', 'Jones', invite.id)
        john.id = 4

        invite.guests = [joe]
        names = Step2InviteDetails(invite).guest_list()
        self.assertEqual(names, "Joe Smith")

        invite.guests = [joe, jane]
        names = Step2InviteDetails(invite).guest_list()
        self.assertEqual(names, "Joe and Jane Smith")

        invite.guests = [joe, jane, jim]
        names = Step2InviteDetails(invite).guest_list()
        self.assertEqual(names, "Joe, Jane and Jim Smith")

        invite.guests = [joe, jane, jim, john]
        names = Step2InviteDetails(invite).guest_list()
        self.assertEqual(names, "John Jones and Joe, Jane and Jim Smith")

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
        self.assertIn(
            'Joe',
            html.xpath('//span[contains(@class, "attending")]/text()')[0]
        )
        self.assertIn(
            'Jane',
            html.xpath('//span[contains(@class, "avoiding")]/text()')[0]
        )

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
                "choice": "Stuffed turkey and ham"
            },
            {
                "name": "Paul",
                "choice": "Vegetable tarte tatin"
            },
            {
                "name": "Ringo",
                "choice": "Roast sirloin of beef"
            }
        ]
        self.assertEqual(expected, FinishedStep(rsvps).menu_choices())
