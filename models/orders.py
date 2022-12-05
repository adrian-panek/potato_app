#!/usr/bin/env python3

from db import db

orders_to_meals = db.Table('orders_to_meals',
                           db.Column('orders_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
                           db.Column('meals_id', db.Integer, db.ForeignKey('meals.id'), primary_key=True))


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    delivery_date = db.Column(db.Integer)  #TODO: change it to proper data type

    meals = db.relationship(
        'MealModel',
        secondary=orders_to_meals,
        backref=db.backref('orders', lazy=True))

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            "delivery_date": self.delivery_date,
            'meals': [item.json() for item in self.meals]
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
