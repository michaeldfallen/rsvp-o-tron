from db import db
import uuid


class Invite(db.Model):
    __tablename__ = 'invite'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String())
    # guests = db.relationship('Guest', order_by="Guest.id", backref="invite")

    def __new_uuid():
        return uuid.uuid4().hex[:6]

    def __init__(self, token=__new_uuid()):  # , guests):
        self.token = token
    #    self.guests = guests

    def __repr__(self):
        return '<Invite (id {})>'.format(self.id)

    @staticmethod
    def all():
        return Invite.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()
