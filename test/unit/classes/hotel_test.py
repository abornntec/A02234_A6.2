'''Archivo para probar la clase Hotel'''


import unittest

from unittest.mock import patch, call
from app.classes.data_handler import DataHandler
from app.classes.hotel import Hotel
from app.classes.reservation import Reservation


class TestHotel(unittest.TestCase):
    '''Calse para probar la clase Hotel'''

    def setUp(self):
        data_handler = DataHandler("test.json")
        self.hotel_instance = Hotel(data_handler)
        self.test_hotel = [{
            "name": "hotel",
            "country": "country",
            "state": "state",
            "address": "address",
            "id": 1
        }]
        self.test_reservation = [{
            "hotel_id": "hotel_id",
            "customer_id": "customer_id",
            "check_in_date": "check_in_date",
            "check_out_date": "check_out_date",
            "Status": "confirmed",
            "id": 1
        }]

    # Test create Hotel
    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'create_registry', return_value=[{
            "name": "hotel",
            "country": "country",
            "state": "state",
            "address": "address",
            "id": 1
    }])
    def test_create_hotel_succesfull(
        self, mock_create_registry, mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento de crear hotel'''
        hotel = self.test_hotel[0].copy()
        del hotel["id"]
        result = self.hotel_instance.create_hotel(
            hotel["name"],
            hotel["country"],
            hotel["state"],
            hotel["address"]
        )
        mock_is_missing.assert_has_calls([
            call(hotel["name"]),
            call(hotel["country"]),
            call(hotel["state"]),
            call(hotel["address"])
        ], any_order=True)
        mock_create_registry.assert_called_once_with(hotel)
        self.assertEqual(result, self.test_hotel)

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_create_hotel_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        hotel = self.test_hotel[0].copy()
        result = self.hotel_instance.create_hotel(
            hotel["name"],
            hotel["country"],
            hotel["state"],
            hotel["address"]
        )
        del hotel["id"]
        mock_is_missing.assert_called()
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    # Test Delete Hotele

    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'delete_from_file', return_value=[])
    def test_delete_hotel_succesfull(
        self,
        mock_delete_from_file,
        mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento del metodo delete hotel'''
        id_to_delete = self.test_hotel[0]["id"]
        deleted_hotel = self.test_hotel.copy()
        del deleted_hotel[0]
        result = self.hotel_instance.delete_hotel(id_to_delete)
        mock_is_missing.assert_called_once_with(id_to_delete)
        mock_delete_from_file.assert_called_once_with(id_to_delete)
        self.assertEqual(result, deleted_hotel)

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_delete_hotel_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        id_to_delete = self.test_hotel[0]["id"]
        result = self.hotel_instance.delete_hotel(id_to_delete)
        mock_is_missing.assert_called_once_with(id_to_delete)
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    # Test get hotel info
    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'get_data_by_id', return_value={
        "name": "hotel",
        "country": "country",
        "state": "state",
        "address": "address",
        "id": 1
    })
    def test_get_hotel_info_succesfull(
        self, mock_get_data_by_id, mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento del metodo get hotel info'''
        expected_info = self.test_hotel[0]
        id_to_get = expected_info["id"]
        result = self.hotel_instance.get_hotel_info(id_to_get)
        mock_is_missing.assert_called_once_with(id_to_get)
        mock_get_data_by_id.assert_called_once_with(id_to_get)
        self.assertEqual(result, expected_info)

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_get_hotel_info_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        id_to_get = self.test_hotel[0]["id"]
        result = self.hotel_instance.get_hotel_info(id_to_get)
        mock_is_missing.assert_called_once_with(id_to_get)
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    # Test Modify hotel

    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'modify_file', return_value=[{
            "name": "modified Name",
            "country": "country",
            "state": "state",
            "address": "address",
            "id": 1
    }])
    def test_modify_hotel_succesfull(self, mock_modify_file, mock_is_missing):
        '''Metodo para verificar
        el correcto
        funcionamiento del metodo modify hotel'''
        hotel_to_modify = self.test_hotel[0].copy()
        hotel_to_modify["name"] = "modified Name"
        result = self.hotel_instance.modify_hotel(hotel_to_modify)
        mock_is_missing.assert_has_calls([
            call(hotel_to_modify["name"]),
            call(hotel_to_modify["country"]),
            call(hotel_to_modify["state"]),
            call(hotel_to_modify["address"]),
            call(hotel_to_modify["id"])
        ], any_order=True)
        mock_modify_file.assert_called_once_with(hotel_to_modify)
        self.assertEqual(result, [hotel_to_modify])

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_modify_hotel_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        hotel_to_modify = self.test_hotel[0].copy()
        hotel_to_modify["name"] = "modified Name"
        result = self.hotel_instance.modify_hotel(hotel_to_modify)
        mock_is_missing.assert_called_once()
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    # Test Create reservation
    @patch.object(Reservation, 'create_reservation', return_value=[{
        "hotel_id": "hotel_id",
        "customer_id": "customer_id",
        "check_in_date": "check_in_date",
        "check_out_date": "check_out_date",
        "Status": "confirmed",
        "id": 1
    }])
    def test_make_reservation_succesfull(self, mock_create_reservation):
        '''Metodo para verificar el
        comportamiento correcto
        del metodo make reservation'''
        reservation_to_make = self.test_reservation[0].copy()
        del reservation_to_make["Status"]
        del reservation_to_make["id"]
        result = self.hotel_instance.make_reservation(
            reservation_to_make["customer_id"],
            reservation_to_make["hotel_id"],
            reservation_to_make["check_in_date"],
            reservation_to_make["check_out_date"]
        )
        mock_create_reservation.assert_called_once_with(
            reservation_to_make,
            self.hotel_instance
        )
        self.assertEqual(result, self.test_reservation)

    @patch.object(
            Reservation,
            'create_reservation',
            return_value=("Hotel or Customer with specified ID does not exist")
    )
    def test_make_reservation_no_id_found(self, mock_create_reservation):
        '''Metodo para verificar que arroja
        ell error correcto cuando no se encuentra
        el hotel o el customer'''
        reservation_to_make = self.test_reservation[0].copy()
        del reservation_to_make["Status"]
        del reservation_to_make["id"]
        result = self.hotel_instance.make_reservation(
            reservation_to_make["customer_id"],
            reservation_to_make["hotel_id"],
            reservation_to_make["check_in_date"],
            reservation_to_make["check_out_date"]
        )
        mock_create_reservation.assert_called_once_with(
            reservation_to_make,
            self.hotel_instance
        )
        self.assertRaises(ValueError)
        self.assertEqual(result, "Failed creating reservation")

    # Test cancel_reservation
    @patch.object(Reservation, 'cancel_reservation', return_value=[{
        "hotel_id": "hotel_id",
        "customer_id": "customer_id",
        "check_in_date": "check_in_date",
        "check_out_date": "check_out_date",
        "Status": "canceled",
        "id": 1
    }])
    def test_cancel_reservation_succesfull(self, mock_cancel_reservation):
        '''Metodo para verificar
        el correcto funcionamiento
        del metodo cancel reservation
        '''
        reservation_to_cancel = self.test_reservation[0].copy()
        id_to_cancel = reservation_to_cancel["id"]
        result = self.hotel_instance.cancel_reservation(id_to_cancel)
        mock_cancel_reservation.assert_called_once_with(id_to_cancel)
        reservation_to_cancel["Status"] = "canceled"
        self.assertEqual(result, [reservation_to_cancel])


if __name__ == "__main__":
    unittest.main()
