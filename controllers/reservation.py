#!/usr/bin/env python3


from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.reservation import ReservationModel
from util.logz import create_logger


class Reservation(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('user_id', type=int, required=True, help='This field cannot be left blank')
    parser.add_argument('room_number', type=int, required=True, help='This field cannot be left blank')
    parser.add_argument('begin_date', type=int, required=True, help='This field cannot be left blank')
    parser.add_argument('end_date', type=int, required=True, help='This field cannot be left blank')

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def delete(self, id):
        reservation = ReservationModel.find_by_id(id)
        if reservation:
            reservation.delete_from_db()
            return {'message': 'Rezerwacja została usunięta z bazy'}, 200

        return {'message': 'Nie ma takiej rezerwacji w bazie danych'}, 404

    @jwt_required()  
    def get(self, id):
        reservation = ReservationModel.find_by_id(id)
        if reservation:
            self.logger.info(f'Rezerwacja: {reservation.json()}')
            return reservation.json()
        return {'message': 'Nie ma takiej rezerwacji w bazie danych'}, 404

    @jwt_required()
    def patch(self, id):
        data = Reservation.parser.parse_args()
        reservation = ReservationModel.find_by_id(id)
        if reservation is None:
            reservation = ReservationModel(**data)
        else:
            reservation.user_id = data['user_id']
            reservation.room_number = data['room_number']
            reservation.begin_date = data['begin_date']
            reservation.end_date = data['end_date']
        reservation.save_to_db()
        return reservation.json()

class ReservationList(Resource):
    @jwt_required()
    def post(self):
        data = Reservation.parser.parse_args()
        reservation = ReservationModel(**data)
        try:
            reservation.save_to_db()
        except:
            return {"message": "Wystąpił błąd podczas dodawania rezerwacji do bazy danych."}, 500
        return reservation.json(), 201

    @jwt_required()
    def get(self):
        return {'reservations': [reservation.json() for reservation in ReservationModel.query.all()]}