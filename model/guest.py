from db import db


class Guest(db.Model):
    __tablename__ = 'guest'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    invite_id = db.Column(db.Integer, db.ForeignKey('invite.id'))

    invite = db.relationship('Invite')

    def __init__(
            self,
            first_name,
            last_name,
            invite_id):
        self.first_name = first_name
        self.last_name = last_name
        self.invite_id = invite_id

    def __repr__(self):
        return '<Guest(id {}, name {}{}, invite {})>'.format(
            self.id,
            self.first_name,
            self.last_name,
            self.invite_id
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
