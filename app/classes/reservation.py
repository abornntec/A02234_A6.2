'''Archivo para crear clase de Reservation'''

import os

from app.classes.customer import Customer
from app.classes.data_handler import DataHandler


class Reservation():
    '''Clase para manejar reservaciones'''

    def __init__(self, data_handler):
        base_dir = os.path.dirname(
            os.path.abspath(__file__)
            )
        customer_file_path = os.path.join(
            base_dir, "..", "data", "customers.json"
            )
        self.data_handler = data_handler
        customer_data_handler = DataHandler(customer_file_path)
        self.customer_instance = Customer(customer_data_handler)

    def create_reservation(
            self, reservation, hotel_instance
            ):
        '''Metodo para crear reservación'''
        try:
            if any(
                self.data_handler.is_missing(reservation[key])
                for key in [
                    "hotel_id",
                    "customer_id",
                    "check_in_date",
                    "check_out_date"
                ]
            ):
                raise ValueError("Missing data")
            customer = self.customer_instance.get_customer_data(
                reservation["customer_id"]
            )
            hotel = hotel_instance.get_hotel_info(
                reservation["customer_id"]
            )
            if (
                customer == "No data found"
                or hotel == "No data found"
            ):
                return "Hotel or Customer with specified ID does not exist"
            reservation = {
                "hotelID": reservation["hotel_id"],
                "CustomerID": reservation["customer_id"],
                "checkInDate": reservation["check_in_date"],
                "checkOutDate": reservation["check_out_date"],
                "Status": "confirmed"
            }
            new_reservation_list = self.data_handler.create_registry(
                reservation
            )
            return new_reservation_list
        except ValueError:
            return "Missing data"

    def cancel_reservation(self, reservation_id):
        '''Metodo para canclar reservación'''
        reservation_to_modify = self.get_reservation_by_id(reservation_id)
        if reservation_to_modify == "No data found":
            return "Id does not exist"
        reservation_to_modify["Status"] = "canceled"
        modified_reservation_list = self.data_handler.modify_file(
            reservation_to_modify
            )
        return modified_reservation_list

    def get_reservation_by_id(self, reservation_id):
        '''Metodo para obtener info de reservación'''
        try:
            if self.data_handler.is_missing(reservation_id):
                raise ValueError("Missing data")
            reservation_info = self.data_handler.get_data_by_id(reservation_id)
            return reservation_info
        except ValueError:
            return "Missing data"
