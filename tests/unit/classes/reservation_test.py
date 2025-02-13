'''Archivo para probar la clase Reservation'''


import unittest

from unittest.mock import patch, call
from app.classes.customer import Customer
from app.classes.data_handler import DataHandler
from app.classes.reservation import Reservation
from app.classes.hotel import Hotel


class TestReservation(unittest.TestCase):
    '''Calse para probar la clase Reservation'''

    def setUp(self):
        data_handler = DataHandler("test.json")
        self.reservation_instance = Reservation(data_handler)
        self.customer_isntance = Customer(data_handler)
        self.hotel_isntance = Hotel(data_handler)
        self.test_reservation = [{
            "hotelID": 1,
            "CustomerID": 1,
            "checkInDate": "check_in_date",
            "checkOutDate": "check_out_date",
            "Status": "confirmed",
            "id": 1
        }]

    # test create_reservation
    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(Customer, 'get_customer_data', return_value={
        "name": "name",
        "lastName": "lastName",
        "id": 1
    })
    @patch.object(Hotel, 'get_hotel_info', return_value=[{
        "name": "name",
        "country": "country",
        "state": "state",
        "address": "address",
        "id": 1
    }])
    @patch.object(DataHandler, 'create_registry', return_value=[{
        "hotelID": 1,
        "CustomerID": 1,
        "checkInDate": "check_in_date",
        "checkOutDate": "check_out_date",
        "Status": "confirmed",
        "id": 1
    }])
    def test_create_reservation_sucesfull(
        self,
        mock_create_registry,
        mock_get_hotel_info,
        mock_get_customer_data,
        mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento de crear reservación'''
        hotel_reservation = {
            "hotel_id": 1,
            "customer_id": 1,
            "check_in_date": "check_in_date",
            "check_out_date": "check_out_date",
            "Status": "confirmed"
        }
        expected_reservation = self.test_reservation[0]
        reservation = expected_reservation.copy()
        del reservation["id"]
        result = self.reservation_instance.create_reservation(
            hotel_reservation,
            self.hotel_isntance
        )
        mock_is_missing.assert_has_calls([
            call(hotel_reservation["hotel_id"]),
            call(hotel_reservation["customer_id"]),
            call(hotel_reservation["check_in_date"]),
            call(hotel_reservation["check_out_date"]),
        ])
        mock_get_customer_data.assert_called_once_with(
            hotel_reservation["customer_id"]
        )
        mock_get_hotel_info.assert_called_once_with(
            hotel_reservation["hotel_id"]
        )
        print(expected_reservation)
        mock_create_registry.assert_called_once_with(reservation)
        self.assertEqual(result, [expected_reservation])

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_create_reservation_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        hotel_reservation = {
            "hotel_id": 1,
            "customer_id": 1,
            "check_in_date": "",
            "check_out_date": "check_out_date",
            "Status": "confirmed"
        }
        result = self.reservation_instance.create_reservation(
            hotel_reservation,
            self.hotel_isntance
        )
        mock_is_missing.assert_called_once()
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(Customer, 'get_customer_data', return_value="No data found")
    @patch.object(Hotel, 'get_hotel_info', return_value=[{
        "name": "name",
        "country": "country",
        "state": "state",
        "address": "address",
        "id": 1
    }])
    def test_create_reservation_customer_not_found(
        self,
        mock_get_hotel_info,
        mock_get_customer_data,
        mock_is_missing
    ):
        '''Metodo para validar
        que arroja el error correcto
        cuando no encuentra el customer'''
        hotel_reservation = {
            "hotel_id": 2,
            "customer_id": 2,
            "check_in_date": "check_in_date",
            "check_out_date": "check_out_date",
            "Status": "confirmed"
        }
        expected_reservation = self.test_reservation[0]
        reservation = expected_reservation.copy()
        del reservation["id"]
        result = self.reservation_instance.create_reservation(
            hotel_reservation,
            self.hotel_isntance
        )
        mock_is_missing.assert_has_calls([
            call(hotel_reservation["hotel_id"]),
            call(hotel_reservation["customer_id"]),
            call(hotel_reservation["check_in_date"]),
            call(hotel_reservation["check_out_date"]),
        ])
        mock_get_customer_data.assert_called_once_with(
            hotel_reservation["customer_id"]
        )
        mock_get_hotel_info.assert_called_once_with(
            hotel_reservation["hotel_id"]
        )
        self.assertEqual(
            result,
            "Hotel or Customer with specified ID does not exist"
        )

    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(Customer, 'get_customer_data', return_value={
        "name": "name",
        "lastName": "lastName",
        "id": 1
    })
    @patch.object(Hotel, 'get_hotel_info', return_value="No data found")
    def test_create_reservation_hotel_not_found(
        self,
        mock_get_hotel_info,
        mock_get_customer_data,
        mock_is_missing
    ):
        '''Metodo para validar
        que arroja el error correcto
        cuando no encuentra el hotel'''
        hotel_reservation = {
            "hotel_id": 2,
            "customer_id": 2,
            "check_in_date": "check_in_date",
            "check_out_date": "check_out_date",
            "Status": "confirmed"
        }
        expected_reservation = self.test_reservation[0]
        reservation = expected_reservation.copy()
        del reservation["id"]
        result = self.reservation_instance.create_reservation(
            hotel_reservation,
            self.hotel_isntance
        )
        mock_is_missing.assert_has_calls([
            call(hotel_reservation["hotel_id"]),
            call(hotel_reservation["customer_id"]),
            call(hotel_reservation["check_in_date"]),
            call(hotel_reservation["check_out_date"]),
        ])
        mock_get_customer_data.assert_called_once_with(
            hotel_reservation["customer_id"]
        )
        mock_get_hotel_info.assert_called_once_with(
            hotel_reservation["hotel_id"]
        )
        self.assertEqual(
            result,
            "Hotel or Customer with specified ID does not exist"
        )

    # test cancel_reservation

    @patch.object(Reservation, 'get_reservation_by_id', return_value={
        "hotelID": 1,
        "CustomerID": 1,
        "checkInDate": "check_in_date",
        "checkOutDate": "check_out_date",
        "Status": "confirmed",
        "id": 1
    })
    @patch.object(DataHandler, 'modify_file', return_value=[{
        "hotelID": 1,
        "CustomerID": 1,
        "checkInDate": "check_in_date",
        "checkOutDate": "check_out_date",
        "Status": "canceled",
        "id": 1
    }])
    def test_cancel_reservation_succesfull(
        self,
        mock_modify_file,
        mock_get_reservation_by_id
    ):
        '''Metodo para verificar el correcto
        funcionamiento del metodo
        cancel reservation'''
        expected_result = {
            "hotelID": 1,
            "CustomerID": 1,
            "checkInDate": "check_in_date",
            "checkOutDate": "check_out_date",
            "Status": "canceled",
            "id": 1
        }
        id_to_modify = self.test_reservation[0]["id"]
        result = self.reservation_instance.cancel_reservation(id_to_modify)
        mock_get_reservation_by_id.assert_called_once_with(id_to_modify)
        mock_modify_file.assert_called_once_with(expected_result)
        self.assertEqual(result, [expected_result])

    @patch.object(
            Reservation,
            'get_reservation_by_id',
            return_value="No data found"
    )
    def test_cancel_reservation_not_found(self, mock_get_reservation_by_id):
        '''Metodo para verificar el correcto
        funcionamiento del metodo
        cancel reservation cuando no
        encunetra la reservación'''
        id_to_modify = self.test_reservation[0]["id"]
        result = self.reservation_instance.cancel_reservation(id_to_modify)
        mock_get_reservation_by_id.assert_called_once_with(id_to_modify)
        self.assertEqual(result, "Id does not exist")

    # get_reservation_by_id

    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'get_data_by_id', return_value={
        "hotelID": 1,
        "CustomerID": 1,
        "checkInDate": "check_in_date",
        "checkOutDate": "check_out_date",
        "Status": "confirmed",
        "id": 1
    })
    def test_get_reservation_by_id_succesfull(
        self, mock_get_data_by_id, mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento del metodo get reservation'''
        expected_info = self.test_reservation[0]
        id_to_get = expected_info["id"]
        result = self.reservation_instance.get_reservation_by_id(id_to_get)
        mock_is_missing.assert_called_once_with(id_to_get)
        mock_get_data_by_id.assert_called_once_with(id_to_get)
        self.assertEqual(result, expected_info)

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_get_reservation_by_missing_value(
        self,
        mock_is_missing
    ):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        id_reservation = self.test_reservation[0]["id"]
        result = self.reservation_instance.get_reservation_by_id(
            id_reservation
        )
        mock_is_missing.assert_called_once_with(id_reservation)
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")


if __name__ == "__main__":
    unittest.main()
