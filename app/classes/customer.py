'''Archivo para crear clase de clientes'''


class Customer():
    '''Clase para manejar clientes'''

    def __init__(self, data_handler):
        self.data_handler = data_handler

    def create_customer(self, name, last_name):
        '''Metodo para crear clientes'''
        try:
            customer = {
                "name": name,
                "lastName": last_name,
            }
            if any(
                self.data_handler.is_missing(customer[key])
                for key in ["name", "lastName"]
            ):
                raise ValueError("Missing data")
            new_customer_list = self.data_handler.create_registry(customer)
            return new_customer_list
        except ValueError:
            return "Missing data"

    def delete_customer(self, customer_id):
        '''Metodo para borrar un cliente'''
        try:
            if (
                self.data_handler.is_missing(customer_id)
            ):
                raise ValueError("Missing data")
            all_customers = self.data_handler.delete_from_file(customer_id)
            return all_customers
        except ValueError:
            return "Missing data"

    def modify_customer(self, customer):
        '''Metodo para modificar un cliente'''
        try:
            if any(
                self.data_handler.is_missing(customer[key])
                for key in ["id", "name", "lastName"]
            ):
                raise ValueError("Missing data")
            all_customers = self.data_handler.modify_file(customer)
            return all_customers
        except ValueError:
            return "Missing data"

    def get_customer_data(self, customer_id):
        '''Metodo para obtener datos de un cliente'''
        try:
            if self.data_handler.is_missing(customer_id):
                raise ValueError("Missing data")
            customer_info = self.data_handler.get_data_by_id(customer_id)
            return customer_info
        except ValueError:
            return "Missing data"
