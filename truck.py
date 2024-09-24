class Truck:
    def __init__(self,departure_time,address="4001 South 700 East",miles=0,packages = None):
        self.miles = miles
        self.address = address
        self.departure_time = departure_time
        if packages is None:
            self.packages = []
        else:
            self.packages = packages
