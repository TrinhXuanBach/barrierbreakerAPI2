import json
from json import JSONEncoder
class Home(JSONEncoder):
    def __init__(self, price, area, number_bathroom, number_bedroom, image, date):
        self.price = price
        self.number_bathroom = number_bathroom
        self.number_bedroom  = number_bedroom
        self.area = area
        self.image = image
        self.date = date

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)