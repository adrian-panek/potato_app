#!/usr/bin/env python3

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.orders import OrderModel
from models.meal import MealModel
from util.logz import create_logger


def get_meals_by_id(meals_id):
        meals = []
        for meal_id in meals_id:
            meal = MealModel.find_by_id(meal_id)
            if meal is None:
                return None, f"Posiłek o id: {meal_id} nie istnieje w bazie danych."
            meals.append(meal)

        return meals, ""


class Order(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('user_id', type=int, required=True)
    parser.add_argument('delivery_date', type=int, required=True)
    parser.add_argument('meals', type=int, action='append', required=True)

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, id):
        Order = OrderModel.find_by_id(id)
        if Order:
            return Order.json()
        return {'message': 'Nie ma takiego zamówienia w bazie'}, 404

    @jwt_required()
    def delete(self, id):
        Order = OrderModel.find_by_id(id)
        if Order:
            Order.delete_from_db()
            return {'message': 'Zamówienie zostało usunięte z Bazy Danych'}, 200
        return {'message': 'Nie ma takiego zamówienia w bazie'}, 404


    @jwt_required()
    def patch(self, id):
        data = Order.parser.parse_args()
        order = OrderModel.find_by_id(id)

        meals, error = get_meals_by_id(data['meals'])

        if meals is None:
            return {"message": error}, 500

        if order is None:
            order = OrderModel(data['user_id'], data['delivery_date'], meals)
        else:
            order.user_id = data['user_id']
            order.delivery_date = data['delivery_date']
            order.meals = meals
        order.save_to_db()
        return order.json()

class OrderList(Resource):
    @jwt_required()
    def get(self):
        return {'Orders': [Order.json() for Order in OrderModel.query.all()]}

    @jwt_required()
    def post(self):
        data = Order.parser.parse_args()
        meals = []

        meals, error = get_meals_by_id(data['meals'])
        if meals is None:
            return {"message": error}, 500

        order = OrderModel(data['user_id'], data['delivery_date'], meals)

        try:
            order.save_to_db()
        except:
            return {"message": "Wystąpił błąd podczas składania zamówienia."}, 500
        return order.json(), 201