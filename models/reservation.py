#!/usr/bin/env python3

from db import db


class ReservationModel(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_number = db.Column(db.Integer)
    
    begin_date = db.Column(db.Integer)  #TODO: change it to proper data type
    end_date = db.Column(db.Integer)  #TODO: change it to proper data type

    # oder_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_number': self.room_number,
            'begin_date': self.begin_date,
            'end_date': self.end_date,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
