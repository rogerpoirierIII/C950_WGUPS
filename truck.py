import datetime
from datetime import timedelta


class Truck:
    def __init__(self,name,departure_time,travel_time = timedelta(0),address="4001 South 700 East",miles=0.0,packages = None):
        self.name = name
        self.miles = miles
        self.address = address
        self.departure_time = departure_time
        self.travel_time = travel_time
        if packages is None:
            self.packages = []
        else:
            self.packages = packages

