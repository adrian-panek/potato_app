#!/usr/bin/env python3
import os
import sys

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from resources.meal import Meal, MealList
from resources.order import Order, OrderList
from resources.reservation import Reservation
from resources.user import UserRegister, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(SCRIPT_DIR, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "Super.Apka.Do.Zamawiania.Ziemniaczkow.Kocham"
jwt = JWTManager(app)
api = Api(app)


@app.before_first_request
def create_tables():
    from db import db
    db.init_app(app)
    db.create_all()

api.add_resource(Meal, '/meal/<string:name>')
api.add_resource(MealList, '/meals')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/login')
api.add_resource(Order, '/order/<int:id>')
api.add_resource(OrderList, '/orders')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  