from functools import reduce
from app.db import db
import uuid


class Invite(db.Model):
    __tablename__ = 'invite'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String())
    guests = db.relationship(
        'Guest',
        order_by='Guest.id',
        backref='invite_guests')

    def __new_uuid(self):
        return uuid.uuid4().hex[:6]

    def __init__(self, token=None):
        self.token = token if token is not None else self.__new_uuid()

    def __repr__(self):
        return '<Invite (id {})>'.format(self.id)

    def is_complete(self):
        def has_guests():
            return len(self.guests) != 0

        def all_have_responded():
            def are_complete(result, guest):
                return (
                    result and
                    guest.rsvp is not None and
                    not guest.rsvp.incomplete()
                )

            return reduce(are_complete, self.guests, True)

        return has_guests() and all_have_responded()

    @staticmethod
    def all():
        return Invite.query.all()

    def get(token):
        invite = Invite.query.filter_by(token=token).first()
        return invite

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def delete(token):
        invite = Invite.get(token)
        db.session.delete(invite)
        db.session.commit()
