from app.db import db
import json


class RSVP(db.Model):
    __tablename__ = 'rsvp'

    id = db.Column(db.Integer, primary_key=True)
    attending = db.Column(db.Boolean(), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))

    guest = db.relationship('Guest')

    def __init__(self, guest_id):
        self.guest_id = guest_id

    def __eq__(self, other):
        return [
            self.id,
            self.attending,
            self.guest_id
        ] == [
            other.id,
            other.attending,
            other.guest_id
        ]

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get(_id):
        return RSVP.query.filter_by(id=_id).first()

    def to_json(self):
        def jdefault(o):
            jsondata = {}

            def append(name, parameter):
                value = parameter(o)
                if value is not None:
                    jsondata[name] = value

            append('guest_id', lambda obj: obj.guest_id)
            append('id', lambda obj: obj.id)
            append('attending', lambda obj: obj.attending)

            return jsondata

        return json.dumps(self, default=jdefault)

    @staticmethod
    def from_json(jsondata):
        def as_rsvp(dct):
            _id = dct.get('id')
            _attending = dct.get('attending')
            _guest_id = dct.get('guest_id')
            rsvp = RSVP(_guest_id)
            rsvp.attending = _attending
            rsvp.id = _id
            return rsvp

        return json.loads(jsondata, object_hook=as_rsvp)

    def __repr__(self):
        return '<RSVP(id {}, guest_id {}, attending{})>'.format(
            self.id,
            self.guest_id,
            self.attending
        )
