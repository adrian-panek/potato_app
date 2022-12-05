#!/usr/bin/env python3

from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user
from models.user import UserModel
from util.encoder import AlchemyEncoder
import json


class User(Resource):
    def __init__(self):
        pass

    parser = reqparse.RequestParser() 
    parser.add_argument('username', type=str, required=True, help='Proszę podać login')
    parser.add_argument('password', type=str, required=True, help='Prosze podać hasło')

    def post(self):
        data = User.parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.query.filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return {'message': 'Niepoprawny login lub hasło.'}, 401
        access_token = create_access_token(identity=json.dumps(user, cls=AlchemyEncoder))
        print(access_token)
        return jsonify(access_token=access_token)

    @jwt_required()
    def get(self):
        return jsonify(
            id=current_user.id,
            full_name=current_user.full_name,
            username=current_user.username,
        )


class UserRegister(Resource):
    def __init__(self):
        pass

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Proszę podać login')
    parser.add_argument('password', type=str, required=True, help='Prosze podać hasło')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Użytkownik z tym loginem już istnieje w bazie danych.'}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'Użytkownik został poprawnie utworzony.'}, 201