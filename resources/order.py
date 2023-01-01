#!/usr/bin/env python3

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.orders import OrderModel
from util.logz import create_logger


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True)
    parser.add_argument('delivery_date', type=int, required=True)

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
        data = Order.parser.parse_args()
        order = OrderModel(id, data['user_id'], data['delivery_date'])
        try:
            order.save_to_db()
        except:
            return {"message": "Wystąpił błąd podczas składania zamówienia."}, 500
        return order.json(), 201

    @jwt_required()
    def delete(self, id):
        Order = OrderModel.find_by_id(id)
        if Order:
            Order.delete_from_db()
        return {'message': 'Zamówienie zostało usunięte z Bazy Danych'}, 204


    @jwt_required()
    def patch(self, id):
        data = Order.parser.parse_args()
        order = OrderModel.find_by_id(id)
        if order is None:
            order = OrderModel(id, data['user_id'], data['delivery_date'])
        else:
            order.user_id = data['user_id']
            order.delivery_date = data['delivery_date']
        order.save_to_db()
        return order.json()


class OrderList(Resource):
    @jwt_required()
    def get(self):
        return {'Orders': [Order.json() for Order in OrderModel.query.all()]}