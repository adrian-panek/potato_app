#!/usr/bin/env python3
import os
import sys
from datetime import timedelta

from flask import Flask
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, unset_jwt_cookies, get_jwt, current_user

from flask_restful import Api

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from controllers.meal import Meal, MealList
from controllers.order import Order, OrderList
from controllers.reservation import Reservation, ReservationList
from controllers.user import UserRegister, User, check_if_token_is_revoked_impl

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(SCRIPT_DIR, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "Super.Apka.Do.Zamawiania.Ziemniaczkow.Kocham"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

jwt = JWTManager(app)
api = Api(app)

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    return check_if_token_is_revoked_impl(jti)

@app.before_first_request
def create_tables():
    from db import db
    db.init_app(app)
    db.create_all()

# example api: https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful

api.add_resource(Meal, '/meals/<int:id>')
api.add_resource(MealList, '/meals')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/login')
api.add_resource(Order, '/orders/<int:id>')
api.add_resource(OrderList, '/orders')
api.add_resource(Reservation, '/reservations/<int:id>')
api.add_resource(ReservationList, '/reservations')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  