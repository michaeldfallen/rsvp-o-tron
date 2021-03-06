from app.db import db
from app import json


class RSVP(db.Model, json.Serialisable):
    __tablename__ = 'rsvp'

    id = db.Column(db.Integer, primary_key=True)
    attending = db.Column(db.Boolean(), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    menu_choice = db.Column(db.String)
    name = db.Column(db.String)

    guest = db.relationship('Guest')

    def __init__(self, guest_id, name):
        self.name = name
        self.guest_id = guest_id

    def __eq__(self, other):
        return [
            self.id,
            self.attending,
            self.name,
            self.guest_id,
            self.menu_choice
        ] == [
            other.id,
            other.attending,
            other.name,
            other.guest_id,
            other.menu_choice
        ]

    def incomplete(self):
        return self.attending is None or (
            self.attending and self.menu_choice is None
        )

    def save(self):
        existing = self.get_by_guest(self.guest_id)
        if existing is not None:
            existing.delete()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(_id):
        return RSVP.query.filter_by(id=_id).first()

    @staticmethod
    def get_by_guest(_guest_id):
        return RSVP.query.filter_by(guest_id=_guest_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def _json_format(o):
        jsondata = {}

        def append(name, parameter):
            value = parameter(o)
            if value is not None:
                jsondata[name] = value

        append('guest_id', lambda obj: obj.guest_id)
        append('id', lambda obj: obj.id)
        append('attending', lambda obj: obj.attending)
        append('menu_choice', lambda obj: obj.menu_choice)
        append('name', lambda obj: obj.name)

        return jsondata

    @staticmethod
    def _object_hook(dct):
        _id = dct.get('id')
        _attending = dct.get('attending')
        _name = dct.get('name')
        _guest_id = dct.get('guest_id')
        _menu_choice = dct.get('menu_choice')
        rsvp = RSVP(_guest_id, _name)
        rsvp.attending = _attending
        rsvp.menu_choice = _menu_choice
        rsvp.id = _id
        return rsvp

    def __repr__(self):
        return (
            '<RSVP(id {}, guest_id {}, name {}, attending {}, menu_choice {})>'
        ).format(
            self.id,
            self.guest_id,
            self.name,
            self.attending,
            self.menu_choice
        )


class RSVPSet(json.Serialisable):

    def __init__(self, invite_id, guests=[]):
        self.invite_id = invite_id
        self.rsvps = [RSVP(guest.id, guest.first_name) for guest in guests]

    def rsvp_for(self, guest_id):
        def by_id(o): return o.guest_id == guest_id

        return next(filter(by_id, self.rsvps))

    def next_rsvp(self):

        def unfinished(o): return o.incomplete()

        unfinished_rsvps = filter(unfinished, self.rsvps)
        rsvp = next(unfinished_rsvps, None)
        if rsvp is not None:
            return {'guest_id': rsvp.guest_id, 'name': rsvp.name.lower()}
        else:
            return None

    @staticmethod
    def _json_format(o):
        return dict(o.__dict__)

    @staticmethod
    def _object_hook(dct):
        _invite_id = dct.get('invite_id')
        _rsvps = dct.get('rsvps')
        rsvpset = RSVPSet(_invite_id)
        rsvpset.rsvps = _rsvps
        return rsvpset

    def __repr__(self):
        return '<RSVPset(invite_id {}, rsvps {})>'.format(
            self.invite_id,
            [rsvp.__repr__() for rsvp in self.rsvps]
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def update_attending(self, guest_id, attending):
        def by_guest_id(o):
            return o.guest_id is guest_id

        next(filter(by_guest_id, self.rsvps)).attending = attending

    def update_menu_choice(self, guest_id, menu_choice):
        def by_guest_id(o):
            return o.guest_id is guest_id

        next(filter(by_guest_id, self.rsvps)).menu_choice = menu_choice

    def save_responses(self):
        for rsvp in self.rsvps:
            rsvp.save()
