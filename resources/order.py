#!/usr/bin/env python3

from flask_restful import Resource
from models.orders import OrderModel
from flask_jwt_extended import jwt_required
from util.logz import create_logger


class Order(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, id):
        Order = OrderModel.find_by_id(id)
        if Order:
            return Order.json()
        return {'message': 'Nie ma takiego zamówienia w bazie'}, 404

    @jwt_required()
    def post(self, id):
        if OrderModel.find_by_id(id):
            return {'message': "Zamówienie z ID: '{}' zostało już złożone.".format(id)}, 400

        Order = OrderModel(id)
        try:
            Order.save_to_db()
        except:
            return {"message": "Wystąpił błąd podczas składania zamówienia."}, 500
        return Order.json(), 201

    @jwt_required()
    def delete(self, id):
        Order = OrderModel.find_by_id(id)
        if Order:
            Order.delete_from_db()
        return {'message': 'Zamówienie zostało usunięte z Bazy Danych'}


class OrderList(Resource):
    @jwt_required()
    def get(self):
        return {'Orders': [Order.json() for Order in OrderModel.query.all()]}