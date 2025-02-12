'''Archivo para crear clase de Hotel'''


import os
from app.classes.reservation import Reservation
from app.classes.data_handler import DataHandler


class Hotel():
    '''Clase para manejar hoteles'''

    def __init__(self, data_handler):
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "..", "data", "reservations.json")
        self.data_handler = data_handler
        reservation_data_handler = DataHandler(file_path)
        self.reservation_instance = Reservation(reservation_data_handler)

    def create_hotel(self, name, country, state, address):
        '''Metodo para crear hotel'''
        try:
            hotel = {
                "name": name,
                "country": country,
                "state": state,
                "address": address,
            }
            if any(
                self.data_handler.is_missing(hotel[key])
                for key in ["name", "country", "state", "address"]
            ):
                raise ValueError("Missing data")
            new_hotel_list = self.data_handler.create_registry(hotel)
            return new_hotel_list
        except ValueError:
            return "Missing data"

    def delete_hotel(self, hotel_id):
        '''Metodo para borrar hotel'''
        try:
            if self.data_handler.is_missing(hotel_id):
                raise ValueError("Missing data")
            all_hotels = self.data_handler.delete_from_file(hotel_id)
            return all_hotels
        except ValueError:
            return "Missing data"

    def get_hotel_info(self, hotel_id):
        '''Metodo para obtener los datos de un hotel'''
        try:
            if self.data_handler.is_missing(hotel_id):
                raise ValueError("Missing data")
            hotel_info = self.data_handler.get_data_by_id(hotel_id)
            return hotel_info
        except ValueError:
            return "Missing data"

    def modify_hotel(self, hotel):
        '''Metodo para modificar un hotel'''
        try:
            if any(
                self.data_handler.is_missing(hotel[key])
                for key in ["id", "name", "country", "state", "address"]
            ):
                raise ValueError("Missing data")
            all_hotels = self.data_handler.modify_file(hotel)
            return all_hotels
        except ValueError:
            return "Missing data"

    def make_reservation(
            self, customer_id, hotel_id, check_in_date, check_out_date
    ):
        '''Metodo para crear
        una reservación'''
        try:
            reservation = {
                "hotel_id": hotel_id,
                "customer_id": customer_id,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            }
            reservation_list = self.reservation_instance.create_reservation(
                reservation, self
            )
            if reservation_list == (
                "Hotel or Customer with specified ID does not exist"
            ):
                raise ValueError
            return reservation_list
        except ValueError:
            return "Failed creating reservation"

    def cancel_reservation(self, reservation_id):
        '''Metodo para cancelar una reservación'''
        reservation_list = self.reservation_instance.cancel_reservation(
            reservation_id
            )
        return reservation_list
