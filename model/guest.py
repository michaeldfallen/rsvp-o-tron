from db import db


class Guest(db.Model):
    __tablename__ = 'guest'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    invite_id = db.Column(db.Integer, db.ForeignKey('invite.id'))

    invite = db.relationship(
        'Invite',
        backref=db.backref('guests', order_by=id)
    )

    def __init__(
            self,
            firstname,
            lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return '<Guest(id {}, name {}{})>'.format(
            self.id,
            self.firstname,
            self.lastname
        )
