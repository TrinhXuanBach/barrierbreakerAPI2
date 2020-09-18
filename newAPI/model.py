import json
from json import JSONEncoder
class Home(JSONEncoder):
    def __init__(self, price, area, number_bathroom, number_bedroom, image, date, address):
        self.price = price
        self.number_bathroom = number_bathroom
        self.number_bedroom  = number_bedroom
        self.area = area
        self.image = image
        self.date = date
        self.address = address

class DataMonth(JSONEncoder):
    def __init__(self, month, data):
        self.month = month
        self.data  = data