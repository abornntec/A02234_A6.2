'''Functionality Test'''
import os

from app.classes.hotel import Hotel
from app.classes.data_handler import DataHandler
from app.classes.customer import Customer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOTEL_FILE_PATH = os.path.join(BASE_DIR, "data", "hotel.json")
CUSTOMER_FILE_PATH = os.path.join(BASE_DIR, "data", "customers.json")

hotelDataHandler = DataHandler(HOTEL_FILE_PATH)
hotelInstance = Hotel(hotelDataHandler)
customerDataHandler = DataHandler(CUSTOMER_FILE_PATH)
customerInstance = Customer(customerDataHandler)


createdHotel1 = hotelInstance.create_hotel(
    "name", "country", "state", "address"
    )
createdHotel2 = hotelInstance.create_hotel(
    "name2", "country2", "state2", "address2"
    )
hotelInstance.delete_hotel(2)
hotelToModify = createdHotel2[0]
hotelToModify["name"] = "modifiedName"
modifiedHotels = hotelInstance.modify_hotel(hotelToModify)
hotelInfo1 = hotelInstance.get_hotel_info(1)
print(hotelInfo1)
hotelInfo2 = hotelInstance.get_hotel_info(4)
print(hotelInfo2)


createdCustomer1 = customerInstance.create_customer("name", "lastName")
createdCustomer2 = customerInstance.create_customer("name2", "lastName2")
customerList = customerInstance.delete_customer(2)
print(createdCustomer2)
customerToModify = customerList[0]
customerToModify["name"] = "modifiedName"
modifiedCustomers = customerInstance.modify_customer(customerToModify)
customerIfo1 = customerInstance.get_customer_data(1)
print(customerIfo1)
customerIfo2 = customerInstance.get_customer_data(5)
print(customerIfo2)

reservation = hotelInstance.make_reservation(
    customerIfo1["id"], hotelInfo1["id"], "23/12/2025", "28/12/2025"
    )
reservation = hotelInstance.make_reservation(
    5, hotelInfo1["id"], "23/12/2025", "28/12/2025"
    )
print(reservation)

reservations = hotelInstance.cancel_reservation(1)
print(reservations)
reservations = hotelInstance.cancel_reservation(4)
print(reservations)
