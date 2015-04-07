from app.db import db


class RSVP(db.Model):
    __tablename__ = 'rsvp'

    id = db.Column(db.Integer, primary_key=True)
    attending = db.Column(db.Boolean(), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))

    guest = db.relationship('Guest')

    def __init__(self, guest_id):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get(_id):
        return RSVP.query.filter_by(id=_id).first()
