from app.db import db


class Guest(db.Model):
    __tablename__ = 'guest'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    invite_id = db.Column(db.Integer, db.ForeignKey('invite.id'))
    is_child = db.Column(db.Boolean())

    invite = db.relationship('Invite')
    rsvp = db.relationship('RSVP', uselist=False, backref='guest_rsvp')

    def __init__(
            self,
            first_name,
            last_name,
            invite_id,
            is_child=False):
        self.first_name = first_name
        self.last_name = last_name
        self.is_child = is_child
        self.invite_id = invite_id

    def __repr__(self):
        return '<Guest(id {}, name {}{}, invite {}, child {})>'.format(
            self.id,
            self.first_name,
            self.last_name,
            self.invite_id,
            self.is_child
        )

    def get(_id):
        return Guest.query.filter_by(id=_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def delete(id_):
        guest = Guest.query.filter_by(id=id_).first()
        db.session.delete(guest)
        db.session.commit()
