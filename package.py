from datetime import timedelta
from inspect import EndOfBlock
import datetime

class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight,special_note = None,status = 'At Hub',delivery_time = timedelta(0)):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self.status = status
        self.delivery_time = delivery_time
    # def __str__(self):
    #     return "%s, %s, %s, %s, %s, %s, %s" % (
    #         self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight,
    def set_status(self,input_time,departure_time):
        if input_time < departure_time:
            self.status ="At Hub"
        elif self.delivery_time < input_time:
            self.status = self.status
        elif self.delivery_time > input_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"