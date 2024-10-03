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

def generate_package_hash_table(file):
    hash_table = HashTable()
    # Reads packages csv file
    with open(file) as data:
        reader = csv.DictReader(data)

        # creates a new package object for each row in csv file
        for row in reader:
            package = Package(row['Package\nID'],row['Address'],row['City '],row['State'],row['Zip'],row['Delivery\nDeadline'],row['Weight\nKILO'],row['page 1 of 1PageSpecial Notes'])
            if package.deadline == "EOD":
                package.deadline = timedelta(hours=21)
            else:
                min =int(package.deadline[3:5])
                hour = int(package.deadline[:-6])
                package.deadline = timedelta(hours=hour,minutes=min)
            hash_table.insert(package.id, package)
        return hash_table

def generate_address_list():
    address_list = []
    with open("distances.csv") as data:
        reader = csv.reader(data)
        next(reader)
        for row in reader:
            row = (row[1])[1:]

            row = row[:-8]
            if row != '':
                address_list.append(row)

    return address_list

def generate_distance_list():
    distance_list = list()
    with open("distances.csv") as data:
        distances = csv.reader(data,delimiter=',')
        next(distances)
        for distance_point in distances:
            distance_list.append(distance_point[2:])
    return distance_list

def get_distance_between(location1,location2):
    distance = distance_list[location1][location2]
    if distance == '':
        distance = distance_list[location2][location1]
    return float(distance)

def map_address(address):
    for index in range(len(address_list)):
        if address_list.__contains__(address):
            return address_list.index(address)

def plot_route(truck):
    travel_list = []
    unvisited_address =[]
    for package in truck.packages:
         if package_table.lookup(str(package)) is not None:
            unvisited_address.append(package_table.lookup(str(package)))
    truck.packages.clear()
    while len(unvisited_address) != 0:
        next_package = None
        min_distance = float('inf')
        for package in unvisited_address:
            distance = get_distance_between(map_address(truck.address),map_address(package.address))
            if distance <= min_distance:
                min_distance = distance
                next_package = package
        truck.miles += min_distance
        route_time = timedelta(minutes=min_distance/18*60)
        truck.travel_time+= route_time
        next_package.delivery_time = truck.departure_time + truck.travel_time
        if next_package.delivery_time < next_package.deadline:
            next_package.status = f"Delivered at {next_package.delivery_time} from {truck.name} "
        else:
            next_package.status = f"LATE, Delivered: {truck.departure_time + truck.travel_time} from {truck.name}"
        truck.packages.append(next_package.id)
        unvisited_address.remove(next_package)
        truck.address = next_package.address
        for package in unvisited_address:
            if package.address == truck.address:
                if truck.departure_time + route_time < package.deadline:
                    package.status = f"Delivered at {truck.departure_time + route_time } from {truck.name}"
                else:
                    package.status = f"LATE, Delivered: {truck.departure_time + truck.travel_time} from {truck.name}"
                truck.packages.append(package.id)
                unvisited_address.remove(package)

def get_package_statuses(time):
    print()
    print(f"STATUS OF ALL PACKAGES AS OF {time}")
    print()
    print("Truck 1 Packages:")
    for i in range(1,len(package_table.table)//2):
        package = package_table.lookup(str(i))
        for packages in truck1.packages:
            if packages == package.id:
                package.set_status(time,truck1.departure_time)
                print(f"Package: {package.id} Status: {package.status}")
    print("Truck 2 packages:")
    for i in range(1,len(package_table.table)//2):
        package = package_table.lookup(str(i))
        for packages in truck2.packages:
            if packages == package.id:
                package.set_status(time,truck2.departure_time)
                print(f"Package: {package.id} Status: {package.status}")
    print("Truck 3 packages:")
    for i in range(1,len(package_table.table)//2):
        package = package_table.lookup(str(i))
        for packages in truck3.packages:
            if packages == package.id:
                package.set_status(time,truck3.departure_time)
                print(f"Package: {package.id} Status: {package.status}")

package_table = generate_package_hash_table("packages.csv")
address_list = generate_address_list()
distance_list = generate_distance_list()
truck1 = Truck('Truck 1',timedelta(hours=8))
truck2 = Truck('Truck 2',timedelta(hours=12))
truck3 = Truck('Truck 3',timedelta(hours=9,minutes=13))
truck1.packages =[1,4,13,14,15,16,19,20,21,29,30,34,39,40]
truck2.packages =[2,3,7,9,10,11,17,18,22,23,24,33,36,38]
truck3.packages =[5,6,8,12,25,26,27,28,31,32,35,37]

plot_route(truck1)
plot_route(truck2)
plot_route(truck3)

total_miles = truck1.miles + truck2.miles + truck3.miles

class Main:
    print("WGUPS")
    print()
    print(f"Total Miles Driven: {total_miles}")
    while True:
        print()
        print("Please Enter a time in HH:MM format, or type \'q\' to quit ")
        choice = input()
        if choice.lower() == 'q':
            break
        try:
            hour = choice[:2]
            minute = choice[-2:]

            input_time = timedelta(hours=int(hour),minutes=int(minute))

            get_package_statuses(input_time)

        except ValueError:
            print("Response not recognized. Please try again")
