'''Archivo para probar la clase Hotel'''


import unittest

from unittest.mock import patch, call
from app.classes.data_handler import DataHandler
from app.classes.customer import Customer


class TestCustomer(unittest.TestCase):
    '''Calse para probar la clase Customer'''

    def setUp(self):
        data_handler = DataHandler("test.json")
        self.customer_instance = Customer(data_handler)
        self.test_customer = [{
            "name": "customer",
            "lastName": "lastName",
            "id": 1
        }]

    # Test create customer
    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'create_registry', return_value=[{
            "name": "customer",
            "lastName": "lastName",
            "id": 1
    }])
    def test_create_customer_succesfull(
        self,
        mock_create_registry,
        mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento de crear Customer'''
        customer = self.test_customer[0].copy()
        del customer["id"]
        result = self.customer_instance.create_customer(
            customer["name"],
            customer["lastName"]
        )
        mock_is_missing.assert_has_calls([
            call(customer["name"]),
            call(customer["lastName"]),
        ], any_order=True)
        mock_create_registry.assert_called_once_with(customer)
        self.assertEqual(result, self.test_customer)

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_create_customer_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        customer = self.test_customer[0].copy()
        del customer["id"]
        result = self.customer_instance.create_customer(
            customer["name"],
            customer["lastName"]
        )
        mock_is_missing.assert_called()
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    # Test delete customer

    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'delete_from_file', return_value=[])
    def test_delete_customer_succesfull(
        self,
        mock_delete_from_file,
        mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento del metodo delete hotel'''
        id_to_delete = self.test_customer[0]["id"]
        deleted_customer = self.test_customer.copy()
        del deleted_customer[0]
        result = self.customer_instance.delete_customer(id_to_delete)
        mock_is_missing.assert_called_once_with(id_to_delete)
        mock_delete_from_file.assert_called_once_with(id_to_delete)
        self.assertEqual(result, deleted_customer)

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_delete_customer_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        id_to_delete = self.test_customer[0]["id"]
        result = self.customer_instance.delete_customer(id_to_delete)
        mock_is_missing.assert_called_once_with(id_to_delete)
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    # Test modify_customer

    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'modify_file', return_value=[{
            "name": "modified Name",
            "lastName": "lastName",
            "id": 1
    }])
    def test_modify_customer_succesfull(
        self,
        mock_modify_file,
        mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento del metodo modify customer'''
        customer_to_modify = self.test_customer[0].copy()
        customer_to_modify["name"] = "modified Name"
        result = self.customer_instance.modify_customer(customer_to_modify)
        mock_is_missing.assert_has_calls([
            call(customer_to_modify["name"]),
            call(customer_to_modify["lastName"]),
            call(customer_to_modify["id"])
        ], any_order=True)
        mock_modify_file.assert_called_once_with(customer_to_modify)
        self.assertEqual(result, [customer_to_modify])

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_modify_customer_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        customer_to_modify = self.test_customer[0].copy()
        customer_to_modify["name"] = "modified Name"
        result = self.customer_instance.modify_customer(customer_to_modify)
        mock_is_missing.assert_called_once()
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")

    # Test get customer data
    @patch.object(DataHandler, 'is_missing', return_value=False)
    @patch.object(DataHandler, 'get_data_by_id', return_value={
        "name": "customer",
        "lastName": "lastName",
        "id": 1
    })
    def test_get_customer_data_succesfull(
        self, mock_get_data_by_id, mock_is_missing
    ):
        '''Metodo para verificar
        el correcto
        funcionamiento del metodo get customer data'''
        expected_info = self.test_customer[0]
        id_to_get = expected_info["id"]
        result = self.customer_instance.get_customer_data(id_to_get)
        mock_is_missing.assert_called_once_with(id_to_get)
        mock_get_data_by_id.assert_called_once_with(id_to_get)
        self.assertEqual(result, expected_info)

    @patch.object(DataHandler, 'is_missing', return_value=True)
    def test_get_customer_data_missing_value(self, mock_is_missing):
        '''Metodo para verificar que se levante la expcion
        correcta al tener información faltante'''
        id_to_get = self.test_customer[0]["id"]
        result = self.customer_instance.get_customer_data(id_to_get)
        mock_is_missing.assert_called_once_with(id_to_get)
        self.assertRaises(ValueError)
        self.assertEqual(result, "Missing data")


if __name__ == "__main__":
    unittest.main()
