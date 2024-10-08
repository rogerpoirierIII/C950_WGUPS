# Roger Poirier ID: 011110021
from datetime import timedelta
from dis import disco, distb
from msilib import add_tables
from os import remove
from struct import pack_into
from time import process_time_ns
from traceback import print_list

from select import select

from hashTable import HashTable
from package import Package
from truck import Truck
import csv

# This function creates a hashtable from the imported package data
def generate_package_hash_table(file):
    hash_table = HashTable()
    # Reads packages csv file
    with open(file) as data:
        reader = csv.DictReader(data)

        # creates a new package object for each row in csv file
        for row in reader:
            package = Package(row['Package\nID'],row['Address'],row['City '],row['State'],row['Zip'],row['Delivery\nDeadline'],row['Weight\nKILO'],row['page 1 of 1PageSpecial Notes'])
            # Changes the deadline attribute to be in time delta
            if package.deadline == "EOD":
                package.deadline = timedelta(hours=21)
            else:
                min =int(package.deadline[3:5])
                hour = int(package.deadline[:-6])
                package.deadline = timedelta(hours=hour,minutes=min)
            # inserts each package into the hash table
            hash_table.insert(package.id, package)
        return hash_table
# This function creates a list of all the addresses that will be used in the map_address function
def generate_address_list():
    # Initialize an empty list.
    address_list = []
    #Reads the distances csv file
    with open("distances.csv") as data:
        reader = csv.reader(data)
        next(reader)
        # Slices each row of the csv file so that only the address that matches exactly to the package addresses are returned
        for row in reader:
            row = (row[1])[1:]

            row = row[:-8]
            # If the row is not empty, add it to the address list
            if row != '':
                address_list.append(row)

    return address_list
# This function creates a matrix of all the distances that will be used in the get_distance_between function
def generate_distance_list():
    # Initializes an empty list
    distance_list = list()
    # Opens distances csv file
    with open("distances.csv") as data:
        distances = csv.reader(data,delimiter=',')
        next(distances)
        # Slices each row to only return everything after the address and appends that to the list.
        for row in distances:
            distance_list.append(row[2:])
    return distance_list
# This functions takes 2 locations in the form of numbers that indicate the index in the distance matrix and returns the value.
# When used with the map_address function, will return the distance between the 2 addresses
def get_distance_between(location1,location2):
    distance = distance_list[location1][location2]
    # If the coordinates return nothing, flip the coordinates
    if distance == '':
        distance = distance_list[location2][location1]
        # Returns the found distance in the data type of float so we can preform other arithmetic operations later
    return float(distance)
# This function takes the string address and returns the index that corresponds to that address
def map_address(address):
    for index in range(len(address_list)):
        if address_list.__contains__(address):
            return address_list.index(address)
# Custom function I developed that implements the nearest neighbor algorithm
# This function takes the list of packages in the truck's packages list and sorts them to the order the truck will deliver the packages
def plot_route(truck):
    # initializes an empty unvisited list
    unvisited_address =[]
    # Takes a package object corresponding to the package ID in the truck's packages list and copies it to the unvisited list
    for package in truck.packages:
         if package_table.lookup(str(package)) is not None:
            unvisited_address.append(package_table.lookup(str(package)))
    # Clears the trucks current packages list so the ordered list can be added later
    truck.packages.clear()
    # While the unvisited list is not empty, finds the minimum distance between the truck's location
    while len(unvisited_address) != 0:
        # Initializes the next package to null and min_distance to infinity
        next_package = None
        min_distance = float('inf')
        # Loops through the unvisited list and finds the minimum distance the truck will need to travel to the next location
        for package in unvisited_address:
            # Calculates the distance between the truck's current location and the package address for each package
            distance = get_distance_between(map_address(truck.address),map_address(package.address))
            if distance <= min_distance:
                min_distance = distance
                next_package = package
        # Once the minimum distance and next package is found, the trucks milage is updated, the travel time is updated, and the packages status changes
        truck.miles += min_distance
        route_time = timedelta(minutes=min_distance/18*60)
        truck.travel_time+= route_time
        next_package.delivery_time = truck.departure_time + truck.travel_time
        # If the package is delivered on time, the package is given a status. If delivered late, the package status is updated to reflect it being late
        if next_package.delivery_time < next_package.deadline:
            next_package.status = f"Delivered at {next_package.delivery_time} from {truck.name} "
        else:
            next_package.status = f"LATE, Delivered: {truck.departure_time + truck.travel_time} from {truck.name}"
        # Adds the packages back to the truck object's packages list
        truck.packages.append(next_package.id)
        # Removes the package from the unvisited list
        unvisited_address.remove(next_package)
        # Updates the truck's current location
        truck.address = next_package.address
        # Loops through the unvisited list and if there is another package with the same address, also delivers that package to the address.
        for package in unvisited_address:
            if package.address == truck.address:
                # Sets the status of the package the same way as before from LINES 110 - 113
                if truck.departure_time + route_time < package.deadline:
                    package.status = f"Delivered at {truck.departure_time + route_time } from {truck.name}"
                else:
                    package.status = f"LATE, Delivered: {truck.departure_time + truck.travel_time} from {truck.name}"
                #Adds the package with the same address to the truck list and then also removes it from the unvisited list.
                truck.packages.append(package.id)
                unvisited_address.remove(package)

# This function accepts an input time and prints the current status of all packages from each truck at the input time.
def get_package_statuses(time):
    print()
    print(f"STATUS OF ALL PACKAGES AS OF {time}")
    print()
    print("Truck 1 Packages:")
    # Iterates through the package hash table and matches the packages to the packages on the truck 1.
    for i in range(1,len(package_table.table)//2):
        package = package_table.lookup(str(i))
        for packages in truck1.packages:
            if packages == package.id:
                # uses the set_status function from the package object to set the status based off of the input time and the truck 1's departure time
                package.set_status(time,truck1.departure_time)
                print(f"Package: {package.id} Status: {package.status}")
    print("Truck 2 packages:")
    # Iterates through the package hash table and matches the packages to the packages on the truck 2.
    for i in range(1,len(package_table.table)//2):
        package = package_table.lookup(str(i))
        for packages in truck2.packages:
            if packages == package.id:
                # uses the set_status function from the package object to set the status based off of the input time and the truck 2's departure time
                package.set_status(time,truck2.departure_time)
                print(f"Package: {package.id} Status: {package.status}")
    print("Truck 3 packages:")
    # Iterates through the package hash table and matches the packages to the packages on the truck 3.
    for i in range(1,len(package_table.table)//2):
        package = package_table.lookup(str(i))
        for packages in truck3.packages:
            if packages == package.id:
                # uses the set_status function from the package object to set the status based off of the input time and the truck 3's departure time
                package.set_status(time,truck3.departure_time)
                print(f"Package: {package.id} Status: {package.status}")

# Initializes the package hash table, address list, and distance matrix
package_table = generate_package_hash_table("packages.csv")
address_list = generate_address_list()
distance_list = generate_distance_list()

# Initializes the 3 Trucks and sets their respective departure time
truck1 = Truck('Truck 1',timedelta(hours=8))
truck2 = Truck('Truck 2',timedelta(hours=12))
truck3 = Truck('Truck 3',timedelta(hours=9,minutes=13))

# Initializes the packages list for each truck
truck1.packages =[1,4,13,14,15,16,19,20,21,29,30,34,39,40]
truck2.packages =[2,3,7,9,10,11,17,18,22,23,24,33,36,38]
truck3.packages =[5,6,8,12,25,26,27,28,31,32,35,37]

# Calls the custom plot route function for each of the 3 trucks
plot_route(truck1)
plot_route(truck2)
plot_route(truck3)

# Calculates the total miles driven between all 3 trucks
total_miles = truck1.miles + truck2.miles + truck3.miles

class Main:
    print("WGUPS")
    print()
    print(f"Total Miles Driven: {total_miles}")
    while True:
        print()
        print("Please Enter a time in HH:MM format, or type \'q\' to quit ")
        choice = input()
        # If user types 'q' or 'Q', application will quit
        if choice.lower() == 'q':
            break
        try:
            # Slices input to formate into proper timedelta format
            hour = choice[:2]
            minute = choice[-2:]

            input_time = timedelta(hours=int(hour),minutes=int(minute))

            get_package_statuses(input_time)
        # This ensures validation of the user's response to be either the 'q' character or a valid time in the proper format
        except ValueError:
            print("Response not recognized. Please try again")
