'''Archivo para probar la clase DataHandler'''


import unittest
import json

from unittest.mock import mock_open, patch
from app.classes.data_handler import DataHandler


class TestDataHandler(unittest.TestCase):
    '''Calse para probar la clase DataHandler'''

    def setUp(self):
        self.data_handler = DataHandler("test.json")
        self.new_data = {"name": "Hernández"}
        self.data_to_modify = {"name": "Hernández", "id": 2}
        self.test_data = [
            {"name": "Andre", "id": 1},
            {"name": "Maximiliano", "id": 2}
        ]

    # Test create_registry
    @patch.object(DataHandler, 'file_as_json', return_value=[
        {"name": "Andre", "id": 1},
        {"name": "Maximiliano", "id": 2}
    ])
    @patch.object(DataHandler, 'write_to_file', return_value=[
        {"name": "Andre", "id": 1},
        {"name": "Maximiliano", "id": 2},
        {"name": "Hernández", "id": 3}
    ])
    @patch.object(DataHandler, 'create_id', return_value=3)
    def test_create_registry_success(
        self, mock_create_id, mock_write_to_file, mock_file_as_json
    ):
        """Test que se agregue exitosamente a un archivo"""
        result = self.data_handler.create_registry(self.new_data)
        expected_file_content = [
            self.test_data[0],
            self.test_data[1],
            self.new_data
        ]
        mock_file_as_json.assert_called_once()
        mock_create_id.assert_called_once_with(expected_file_content)
        mock_write_to_file.assert_called_once_with(expected_file_content)
        self.assertEqual(result, expected_file_content)

    @patch.object(DataHandler, 'file_as_json', return_value=[])
    @patch.object(DataHandler, 'write_to_file', return_value=[
        {"name": "Hernández", "id": 1}
    ])
    @patch.object(DataHandler, 'create_id', return_value=1)
    def test_create_registry_empty_file(
        self, mock_create_id, mock_write_to_file, mock_file_as_json
    ):
        """Test agregar un registro cuando el archivo no tiene un registro"""
        result = self.data_handler.create_registry(self.new_data)
        expected_file_content = [self.new_data]
        mock_file_as_json.assert_called_once()
        mock_create_id.assert_called_once()
        mock_write_to_file.assert_called_once_with(expected_file_content)
        self.assertEqual(result, expected_file_content)

    # Test modify_file
    @patch.object(DataHandler, 'file_as_json', return_value=[
        {"name": "Andre", "id": 1},
        {"name": "Maximiliano", "id": 2}
    ])
    @patch.object(DataHandler, 'find_index_of_array', return_value=1)
    @patch.object(DataHandler, 'write_to_file', return_value=[
        {"name": "Andre", "id": 1},
        {"name": "Hernández", "id": 2}
    ])
    def test_modify_file_found_index(
        self, mock_write_to_file, mock_find_index_of_array, mock_file_as_json
    ):
        """Test modificar un registro con id encontrado"""
        result = self.data_handler.modify_file(self.data_to_modify)
        expected_file_content = [self.test_data[0], self.data_to_modify]
        expected_id = 2
        mock_file_as_json.assert_called_once()
        mock_find_index_of_array.assert_called_once_with(
            expected_file_content, expected_id
        )
        mock_write_to_file.assert_called_once_with(
            expected_file_content
        )
        self.assertEqual(result, expected_file_content)

    @patch.object(DataHandler, 'file_as_json', return_value=[
        {"name": "Andre", "id": 1}
    ])
    @patch.object(DataHandler, 'find_index_of_array', return_value=-1)
    def test_modify_file_not_found(
        self, mock_find_index_of_array, mock_file_as_json
    ):
        """Test no modificar un registro si el id no es encontrado"""
        result = self.data_handler.modify_file(self.data_to_modify)
        expected_file_content = [self.test_data[0]]
        expected_id = 2
        mock_file_as_json.assert_called_once()
        mock_find_index_of_array.assert_called_once_with(
            expected_file_content, expected_id
        )
        self.assertEqual(result, expected_file_content)

    # Test get Data by id

    @patch.object(DataHandler, 'file_as_json', return_value=[
        {"name": "Andre", "id": 1},
        {"name": "Maximiliano", "id": 2}
    ])
    @patch.object(DataHandler, 'find_index_of_array', return_value=1)
    def test_get_data_by_id_found(
        self, mock_find_index_of_array, mock_file_as_json
    ):
        """Test que entrega la data del archivo que tenga el id"""
        result = self.data_handler.get_data_by_id(2)
        expected_data = self.test_data[1]
        expected_id = 2
        mock_file_as_json.assert_called_once()
        mock_find_index_of_array.assert_called_once_with(
            self.test_data, expected_id
        )
        self.assertEqual(result, expected_data)

    @patch.object(DataHandler, 'file_as_json', return_value=[
        {"name": "Andre", "id": 1},
        {"name": "Maximiliano", "id": 2}
    ])
    @patch.object(DataHandler, 'find_index_of_array', return_value=-1)
    def test_get_data_by_id_not_found(
        self, mock_find_index_of_array, mock_file_as_json
    ):
        """Test que entregue el mensaje de no data encontrada"""
        result = self.data_handler.get_data_by_id(3)
        expected_data = "No data found"
        expected_id = 3
        mock_file_as_json.assert_called_once()
        mock_find_index_of_array.assert_called_once_with(
            self.test_data, expected_id
        )
        self.assertEqual(result, expected_data)

    # Test Delete from File
    @patch.object(DataHandler, 'file_as_json', return_value=[
        {"name": "Andre", "id": 1},
        {"name": "Maximiliano", "id": 2}
    ])
    @patch.object(DataHandler, 'delete_from_json', return_value=[
        {"name": "Andre", "id": 1}
    ])
    @patch.object(DataHandler, 'write_to_file', return_value=[
        {"name": "Andre", "id": 1}
    ])
    def test_delete_from_file_success(
        self, mock_write_to_file, mock_delete_from_json, mock_file_as_json
    ):
        """Test que borre del archivo de manera exitosa"""
        result = self.data_handler.delete_from_file(2)
        expected_data = [{"name": "Andre", "id": 1}]
        mock_file_as_json.assert_called_once()
        mock_delete_from_json.assert_called_once_with(2, self.test_data)
        mock_write_to_file.assert_called_once_with(expected_data)
        self.assertEqual(result, expected_data)

    # Test file as json
    @patch(
            "builtins.open",
            new_callable=mock_open,
            read_data=(
                '[{"name": "Andre", "id": 1},{"name": "Maximiliano","id":2}]'
                )
            )
    def test_file_as_json_success(self, mock_file):
        """Test que el json leido sea el correcto"""
        result = self.data_handler.file_as_json()
        mock_file.assert_called_once()
        self.assertEqual(result, self.test_data)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_as_json_file_not_found(self, mock_file):
        """Test que maneje de manera correcta el error FileNotFoundError"""
        result = self.data_handler.file_as_json()
        mock_file.assert_called_once()
        self.assertEqual(result, "File Does not exists")

    @patch("builtins.open", new_callable=mock_open, read_data="[")
    def test_file_as_json_invalid_json(self, mock_file):
        """Test que maneje de manera correcta
        el error json.decoder.JSONDecodeError"""
        with self.assertRaises(json.decoder.JSONDecodeError):
            self.data_handler.file_as_json()
            mock_file.assert_called_once()

    # Test Filter Json File
    def test_filter_json_file_succesfull(self):
        """Test de filtrar objetos de un json"""
        json_to_filter = self.test_data
        filtered_json = self.data_handler.filter_json_file(1, json_to_filter)
        self.assertEqual(len(filtered_json), 1)
        self.assertEqual(filtered_json, [{"name": "Andre", "id": 1}])

    def test_filter_json_file_not_found(self):
        """Test de filtrar objetos de un json"""
        json_to_filter = self.test_data
        filtered_json = self.data_handler.filter_json_file(4, json_to_filter)
        self.assertEqual(len(filtered_json), 0)

    # Test delete from json
    def test_delete_from_json_item_deleted(self):
        """Test que borre el indice dl id del json"""
        json_to_delete = self.test_data
        id_to_delete = 2
        deleted_json = self.data_handler.delete_from_json(
            id_to_delete, json_to_delete
        )
        self.assertNotIn(
            {"name": "Maximiliano", "id": 2}, deleted_json
        )

    # Test find index of Array
    def test_find_index_of_array_found_index(self):
        """Test que encuentre el indice del id proporcionado"""
        json_to_filter = self.test_data
        index = self.data_handler.find_index_of_array(json_to_filter, 1)
        self.assertEqual(index, 0)

    def test_find_index_of_array_not_found_index(self):
        """Test que eregrese -1 cuando no encuentra el id"""
        json_to_filter = self.test_data
        index = self.data_handler.find_index_of_array(json_to_filter, 4)
        self.assertEqual(index, -1)

    # Test write to file
    @patch(
            "builtins.open",
            new_callable=mock_open,
            read_data=(
                '[{"name": "Andre", "id": 1},{"name": "Maximiliano","id":2}]'
            )
        )
    def test_write_to_file_success(self, mock_file):
        """Test de que se escribe de manera correcta al archivo"""
        result = self.data_handler.write_to_file(self.test_data)
        mock_file.assert_any_call("test.json", "w", encoding="utf-8")
        self.assertEqual(result, self.test_data)

    @patch("builtins.open", side_effect=TypeError)
    def test_write_to_file_failure(self, mock_file):
        """Test de write_to_file maneja errores"""
        result = self.data_handler.write_to_file(self.test_data)
        mock_file.assert_called_once()
        self.assertRaises(TypeError)
        self.assertEqual(result, "Error writing to file")

    # Test create ID
    def test_create_id_succesfull(self):
        '''Metod to test creation of id'''
        result = self.data_handler.create_id(self.test_data)
        self.assertEqual(result, 3)

    def test_create_id_empty(self):
        '''Metod to test creation of id when file is empty'''
        result = self.data_handler.create_id([])
        self.assertEqual(result, 1)

    # Test is missing
    def test_is_missing_no_missing(self):
        '''Metodo para verificar que regresa
        false si el valor no es nulo o vacio'''
        result = self.data_handler.is_missing("test")
        self.assertEqual(result,False)

    def test_is_missing_None(self):
        '''Metodo para verificar que regresa
        true si el valor es nulo'''
        result = self.data_handler.is_missing(None)
        self.assertEqual(result,True)

    def test_is_missing_empty(self):
        '''Metodo para verificar que regresa
        true si el valor es vacio'''
        result = self.data_handler.is_missing("")
        self.assertEqual(result,True)


if __name__ == "__main__":
    unittest.main()
