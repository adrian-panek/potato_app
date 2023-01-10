#!/usr/bin/env python3

from datetime import datetime, timezone

from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import get_jwt, create_access_token, jwt_required, unset_jwt_cookies, current_user
from models.user import UserModel
from models.token_blocklist import TokenBlocklist
from util.encoder import AlchemyEncoder
import json

def check_if_token_is_revoked_impl(jti):
    token = TokenBlocklist.find_by_jti(jti)
    return token is not None

class User(Resource):
    def __init__(self):
        pass

    parser = reqparse.RequestParser(bundle_errors=True) 
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
        return jsonify(access_token=access_token)

    @jwt_required()
    def get(self):
        return jsonify(
            id=current_user.id,
            full_name=current_user.full_name,
            username=current_user.username,
        )

    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        blocked_token = TokenBlocklist(jti=jti, created_at=now)
        blocked_token.save_to_db()
        response = jsonify(message="Nastapilo poprawne wylogowanie uzytkownika")
        unset_jwt_cookies(response)
        return response

class UserRegister(Resource):
    def __init__(self):
        pass

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username', type=str, required=True, help='Proszę podać login')
    parser.add_argument('password', type=str, required=True, help='Prosze podać hasło')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Użytkownik z tym loginem już istnieje w bazie danych.'}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'Użytkownik został poprawnie utworzony.'}, 201