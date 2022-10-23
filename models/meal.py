#!/usr/bin/env python3

from db import db


class MealModel(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    potato_quantity = db.Column(db.Integer())
    meal_type = db.Column(db.String(500))
    diary_addons = db.Column(db.String(500))
    protein_addons = db.Column(db.String(500))

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship('OrderModel')

    def __init__(self, name, price, order_id):
        self.name = name
        self.price = price
        self.order_id = order_id

    def json(self):
        return {
            'name': self.name,
            'price': self.price,
            'order_id': self.order_id,
            'potato_quantity': self.potato_quantity,
            'meal_type': self.meal_type,
            'diary_addons': self.diary_addons,
            'protein_addons': self.protein_addons,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
