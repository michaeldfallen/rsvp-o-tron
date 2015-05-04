import unittest
from test.helpers import with_client, setUpApp
from test.helpers import with_context, setUpDB, tearDownDB
from lxml.html import document_fromstring
from app.invite.model import Invite
from app.guest.model import Guest
from app.rsvp.model import RSVPSet
from flask import session, url_for


class TestRoutes(unittest.TestCase):

    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @staticmethod
    def make_guest():
        invite = Invite()
        invite.save()

        guest = Guest('John', 'Smith', invite.id)
        guest.save()
        return invite, guest

    @with_context
    @with_client
    def test_start_route(self, client):
        res = client.get('/rsvp')
        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_find_invite_fail(self, client):
        res = client.post('/rsvp', data={'token': 'shouldfail'})
        html = document_fromstring(res.get_data())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            html.xpath("//div[@class='error']/text()"),
            ["We couldn't find your invitation"]
        )

    @with_context
    @with_client
    def test_find_invite_found(self, client):
        (invite, guest) = self.make_guest()
        res = client.post('/rsvp', data={'token': invite.token})
        self.assertEqual(res.status_code, 302)
        self.assertTrue(
            res.location.endswith('/rsvp/'+invite.token+'/invite-details')
        )

    @with_context
    @with_client
    def test_invite_details(self, client):
        (invite, guest) = self.make_guest()
        res = client.get('/rsvp/'+invite.token+'/invite-details')
        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_begin_responding(self, client):
        (invite, guest) = self.make_guest()
        res = client.post(
            '/rsvp/'+invite.token+'/invite-details'
        )
        self.assertEqual(res.status_code, 302)
        rsvpset = RSVPSet.from_json(session['rsvp'])

        self.assertEqual(len(rsvpset.rsvps), 1)
        self.assertEqual(rsvpset.invite_id, invite.id)

        rsvp = rsvpset.rsvps[0]
        self.assertEqual(rsvp.attending, None)
        self.assertEqual(rsvp.guest_id, guest.id)

        name = guest.first_name.lower()
        guest_id = str(guest.id)
        self.assertIn(
            '/rsvp/'+invite.token+'/'+guest_id+'/'+name+'/attending',
            res.location
        )

    @with_context
    @with_client
    def test_respond_attending(self, client):
        (invite, guest) = self.make_guest()
        res = client.get(url_for('rsvp.attending',
                                 token=invite.token,
                                 guest_id=guest.id,
                                 name=guest.first_name.lower()))

        html = document_fromstring(res.get_data())
        self.assertEqual(res.status_code, 200)
        self.assertIn(
            "{} {}".format(guest.first_name, guest.last_name),
            html.xpath("//h1/text()")[0]
        )

        with client.session_transaction() as sesh:
            rsvpset = RSVPSet(invite.id, invite.guests)
            sesh['rsvp'] = rsvpset.to_json()
            sesh.modified = True

        res = client.post(
            url_for('rsvp.attending',
                    token=invite.token,
                    guest_id=guest.id,
                    name=guest.first_name.lower()),
            data={'attending': 'true'}
        )
        self.assertEqual(res.status_code, 302)
        self.assertIn(url_for('rsvp.confirm', token=invite.token),
                      res.location)

        rsvpset = RSVPSet.from_json(session['rsvp'])
        rsvp = rsvpset.rsvps[0]
        self.assertEqual(rsvp.attending, True)
        self.assertEqual(rsvp.guest_id, guest.id)
        self.assertEqual(rsvp.name, guest.first_name)

        with client.session_transaction() as sesh:
            rsvpset = RSVPSet(invite.id, invite.guests)
            sesh['rsvp'] = rsvpset.to_json()
            sesh.modified = True

        res = client.post(
            url_for('rsvp.attending',
                    token=invite.token,
                    guest_id=guest.id,
                    name=guest.first_name.lower()),
            data={'attending': 'false'}
        )
        self.assertEqual(res.status_code, 302)
        self.assertIn(url_for('rsvp.confirm', token=invite.token),
                      res.location)

        rsvpset = RSVPSet.from_json(session['rsvp'])
        rsvp = rsvpset.rsvps[0]
        self.assertEqual(rsvp.attending, False)
        self.assertEqual(rsvp.guest_id, guest.id)
        self.assertEqual(rsvp.name, guest.first_name)
