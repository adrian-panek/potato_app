#!/usr/bin/env python3

from db import db


class ReservationModel(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_number = db.Column(db.Integer)
    oder_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # @classmethod
    # def find_by_username(cls, username):
    #     return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
