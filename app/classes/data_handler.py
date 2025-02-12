'''Archivo para crear clase de DataHandler'''

import json


class DataHandler():
    '''Clase para manejar datos en los archivos'''

    def __init__(self, file):
        self.file = file

    def create_registry(self, data):
        '''Metodo para crear un nuevo registro en el archivo'''
        file_json = self.file_as_json()
        my_id = self.create_id(file_json)
        data["id"] = my_id
        file_json.append(data)
        file_json = self.write_to_file(file_json)
        return file_json

    def modify_file(self, data):
        '''Metodo para modificar un registro en el archivo'''
        my_id = data["id"]
        file_json = self.file_as_json()
        index = self.find_index_of_array(file_json, my_id)
        if index < 0:
            return file_json
        file_json[index] = data
        file_json = self.write_to_file(file_json)
        return file_json

    def get_data_by_id(self, my_id):
        '''Metodo para obtener un registro del archivo'''
        file_json = self.file_as_json()
        index = self.find_index_of_array(file_json, my_id)
        if index < 0:
            return "No data found"
        data = file_json[index]
        return data

    def delete_from_file(self, my_id):
        '''Metodo para borrar un registro del archivo'''
        file_json = self.file_as_json()
        json_file = self.delete_from_json(my_id, file_json)
        self.write_to_file(json_file)
        return json_file

    def file_as_json(self):
        '''Metodo para leer al archivo y convertirlo a json'''
        try:
            with open(self.file, encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                return json_data
        except FileNotFoundError:
            print("File does not exists")
            return "File Does not exists"
        except json.decoder.JSONDecodeError as e:
            print("Empty Json, give propper format to file")
            raise e

    def filter_json_file(self, my_id, json_file):
        '''Metodo para filtrar un json
        y obtener los registros con un id especifico'''
        filtered_data = [x for x in json_file if x['id'] == my_id]
        return filtered_data

    def delete_from_json(self, my_id, json_file):
        '''Metodo para borrar un elmento especifico del json'''
        index = self.find_index_of_array(json_file, my_id)
        del json_file[index]
        return json_file

    def find_index_of_array(self, json_file, my_id):
        '''Metodo para obtener el indice del
        registro con el id proporcionado'''
        for i, dic in enumerate(json_file):
            if dic["id"] == my_id:
                return i
        return -1

    def write_to_file(self, original_json_file):
        '''Metodo para escribir en el archivo'''
        try:
            with open(self.file, "w", encoding="utf-8") as json_file:
                json.dump(original_json_file, json_file)
            with open(self.file, encoding="utf-8") as json_file:
                return json.load(json_file)
        except TypeError:
            print("Error writing to file")
            return "Error writing to file"

    def create_id(self, json_file):
        '''Metodo para crear un ID'''
        my_id = 1
        if len(json_file) < 1:
            return my_id
        my_id = json_file[len(json_file) - 1]["id"] + 1
        return my_id

    def is_missing(self, value):
        '''Metodo para validar si un dato viene vacio'''
        return value is None or value == ""
