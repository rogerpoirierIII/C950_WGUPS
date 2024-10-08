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
    # Function sets takes the user input time and the truck's departure time and updates the status of the package
    def set_status(self,input_time,departure_time):
        # Hardcoded solution for package 9 which has the wrong address listed.
        if self.id == 9:
            change_time = timedelta(hours=10, minutes=20)
            # If the users input time is the same or after 10:20am, package 9's address changes to the correct address
            if input_time >= change_time:
                self.address = '410 S State St'
                self.city = 'Salt Lake City'
                self.state = 'UT'
                self.zip = '84111'

        if input_time < departure_time:
            self.status ="At Hub"
        elif self.delivery_time < input_time:
            self.status = self.status
        elif self.delivery_time > input_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"