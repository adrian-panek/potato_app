#!/usr/bin/env python3

from flask_restful import Resource
from models.orders import OrderModel
from flask_jwt_extended import jwt_required


class Order(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, name):
        Order = OrderModel.find_by_name(name)
        if Order:
            return Order.json()
        return {'message': 'Order not found'}, 404

    @jwt_required()
    def post(self, name):
        if OrderModel.find_by_name(name):
            return {'message': "A Order with name '{}' already exists.".format(name)}, 400

        Order = OrderModel(name)
        try:
            Order.save_to_db()
        except:
            return {"message": "An error occurred creating the Order."}, 500
        return Order.json(), 201

    @jwt_required()
    def delete(self, name):
        Order = OrderModel.find_by_name(name)
        if Order:
            Order.delete_from_db()
        return {'message': 'Order deleted'}


class OrderList(Resource):
    @jwt_required()
    def get(self):
        return {'Orders': [Order.json() for Order in OrderModel.query.all()]}