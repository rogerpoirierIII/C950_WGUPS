# Roger Poirier ID: 011110021
from dis import disco
from struct import pack_into
from traceback import print_list

from select import select

from hashTable import HashTable
from package import Package
from truck import Truck
import csv

def generate_package_Hash_Table(file):
    hash_table = HashTable()
    # Reads packages csv file
    with open(file) as data:
        reader = csv.DictReader(data)

        # creates a new package object for each row in csv file
        for row in reader:
            package = Package(row['Package\nID'],row['Address'],row['City '],row['State'],row['Zip'],row['Delivery\nDeadline'],row['Weight\nKILO'],row['page 1 of 1PageSpecial Notes'])
            hash_table.insert(package.id, package)
        return hash_table

def generate_address_list():
    address_list = ['HUB']
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
    for index in range(address_list.__len__()):
        if address_list.__contains__(address):
            return address_list.index(address)

def plot_route(truck):

    route_list = []
    travel_list = []
    unvisited_address =[]
    for package in truck.packages:
         if package_table.lookup(str(package)) is not None:
            unvisited_address.append(package_table.lookup(str(package)))
    while len(unvisited_address) != 0:
        curr_loc = 'HUB'
        next_loc = None
        min_distance = float('inf')
        for i in range(len(unvisited_address)):
            selected_address = unvisited_address[i]

            if curr_loc =='HUB':
                distance = (get_distance_between(0,map_address(selected_address.address)))
            else:
                distance = get_distance_between(map_address(curr_loc),map_address(selected_address.address))

            if distance < min_distance:
                min_distance = distance
                next_loc = selected_address

        route_list.append(next_loc.id)
        travel_list.append(min_distance)
        unvisited_address.remove(next_loc)
        curr_loc = next_loc
    print(route_list)
    print(travel_list)
package_table = generate_package_Hash_Table("packages.csv")
address_list = generate_address_list()
distance_list = generate_distance_list()
truck1 = Truck(1)
truck2 = Truck(1)
truck3 = Truck(1)

truck1.packages =[4, 11, 12, 13, 14, 15, 16, 19, 20, 21, 23, 27, 34, 35, 39, 40]
truck2.packages =[2, 3, 6, 9, 10, 17, 18, 22, 25, 26, 28, 31, 32, 33, 36, 38]
truck3.packages =[1, 5, 7, 8, 24, 29, 30, 37]

plot_route(truck1)
plot_route(truck2)
plot_route(truck3)