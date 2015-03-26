from db import db


class Invite(db.Model):
    __tablename__ = 'invite'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    # guests = db.relationship('Guest', order_by="Guest.id", backref="invite")

    def __init__(self, url):  # , guests):
        self.url = url
    #    self.guests = guests

    def __repr__(self):
        return '<Invite (id {})>'.format(self.id)

    @staticmethod
    def all():
        Invite.query
