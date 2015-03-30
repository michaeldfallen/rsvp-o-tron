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
            lastname,
            invite_id):
        self.firstname = firstname
        self.lastname = lastname
        self.invite_id = invite_id

    def __repr__(self):
        return '<Guest(id {}, name {}{}, invite {})>'.format(
            self.id,
            self.firstname,
            self.lastname,
            self.invite_id
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
