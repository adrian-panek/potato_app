#!/usr/bin/env python3

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.meal import MealModel
from util.logz import create_logger


class Meal(Resource):
    parser = reqparse.RequestParser()  
    parser.add_argument('price', type=float, required=True, help='Należy podać cenę!')
    parser.add_argument('potato_quantity', type=int, required=True, help='Należy podać ilość ziemniaków!')
    parser.add_argument('meal_type', type=str, required=True, help='Należy podać typ dania!')
    parser.add_argument('diary_addons', type=str, required=False)
    parser.add_argument('protein_addons', type=str, required=False)

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  
    def get(self, name):
        meal = MealModel.find_by_name(name)
        self.logger.info(f'Posiłek: {meal.json()}')
        if meal:
            return meal.json()
        return {'message': 'Nie ma takiego posiłku w bazie danych'}, 404

    @jwt_required()
    def post(self, name):
        self.logger.info(f'parsed args: {Meal.parser.parse_args()}')
        if MealModel.find_by_name(name):
            return {'message': "Posiłek z nazwą: '{}' już istnieje w bazie danych.".format(name)}, 400
        data = Meal.parser.parse_args()
        meal = MealModel(name, data['price'], data['potato_quantity'], data['meal_type'], data['diary_addons'], data['protein_addons'])
        try:
            meal.save_to_db()
        except:
            return {"message": "Wystąpił błąd podczas dodawania posiłku do bazy danych."}, 500
        return meal.json(), 201

    @jwt_required()
    def delete(self, name):
        meal = MealModel.find_by_name(name)
        if meal:
            meal.delete_from_db()
            return {'message': 'Posiłek został usunięty z bazy'}

    @jwt_required()
    def put(self, name):
        data = Meal.parser.parse_args()
        meal = MealModel.find_by_name(name)
        if meal is None:
            meal = MealModel(name, data['price'], data['potato_quantity'], data['meal_type'], data['diary_addons'], data['protein_addons'])
        else:
            meal.price = data['price']
            meal.potato_quantity = data['potato_quantity']
            meal.meal_type = data['meal_type']
            meal.diary_addons = data['diary_addons']
            meal.protein_addons = data['protein_addons']
        meal.save_to_db()
        return meal.json()


class MealList(Resource):
    @jwt_required()
    def get(self):
        return {'meals': [meal.json() for meal in MealModel.query.all()]}  # More pythonic