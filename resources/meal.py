#!/usr/bin/env python3

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.meal import MealModel


class Meal(Resource):
    parser = reqparse.RequestParser()  
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True, help='Must enter the store id')

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  
    def get(self, name):
        meal = MealModel.find_by_name(name)
        self.logger.info(f'returning meal: {meal.json()}')
        if meal:
            return meal.json()
        return {'message': 'Meal not found'}, 404

    @jwt_required()
    def post(self, name):
        self.logger.info(f'parsed args: {Meal.parser.parse_args()}')

        if MealModel.find_by_name(name):
            return {'message': "An meal with name '{}' already exists.".format(name)}, 400
        data = Meal.parser.parse_args()
        meal = MealModel(name, data['price'], data['store_id'])

        try:
            meal.save_to_db()
        except:
            return {"message": "An error occurred inserting the meal."}, 500
        return meal.json(), 201

    @jwt_required()
    def delete(self, name):

        meal = MealModel.find_by_name(name)
        if meal:
            meal.delete_from_db()

            return {'message': 'meal has been deleted'}

    @jwt_required()
    def put(self, name):
        data = Meal.parser.parse_args()
        meal = MealModel.find_by_name(name)

        if meal is None:
            meal = MealModel(name, data['price'])
        else:
            meal.price = data['price']

        meal.save_to_db()

        return meal.json()


class MealList(Resource):
    @jwt_required()
    def get(self):
        return {'meals': [meal.json() for meal in MealModel.query.all()]}  # More pythonic