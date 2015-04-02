from app.db import db


class RSVP(db.Model):
    __tablename__ = 'rsvp'

    id = db.Column(db.Integer, primary_key=True)
    attending = db.Column(db.Boolean(), nullable=False)
