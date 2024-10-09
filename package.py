from datetime import timedelta
from inspect import EndOfBlock
import datetime

class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight,special_note = None,status = 'At Hub',delivery_time = timedelta(0),delivery_message = None):
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
        self.delivery_message = delivery_message
    # Function sets takes the user input time and the truck's departure time and updates the status of the package
    def set_status(self,input_time,departure_time):
        if input_time < departure_time:
            self.status ="At Hub"
            # Added validation for packages with the special constraint of not being in the hub until 9:05
            if input_time < timedelta(hours=9,minutes=5) and self.special_note == 'Delayed on flight---will not arrive to depot until 9:05 am':
                self.status = self.special_note
        # Changes the status back to the original delivery message given in the plot route function
        elif self.delivery_time < input_time:
            self.status = self.delivery_message
        elif self.delivery_time > input_time:
            self.status = "En Route"