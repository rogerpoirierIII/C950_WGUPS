# Roger Poirier ID: 011110021
from traceback import print_list

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
            package = Package(row['Package\nID'],row['Address'],row['City '],row['State'],row['Zip'],row['Delivery\nDeadline'],row['Weight\nKILO'])
            hash_table.insert(package.id, package)
        return hash_table

def generate_address_list():
    address_list = list()
    with open("distances.csv") as data:
        reader = csv.reader(data)
        reader = next(reader)
        counter = 0
        for row in reader[2:]:
            address_list.append(counter)
            address_list.append(row)
            counter+=1

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
    return distance

def get_address(address):
    for index in range(address_list.__len__()):
        if address == address_list[index]:
            return address_list[index+1]


package_table = generate_package_Hash_Table("packages.csv")
address_list = generate_address_list()
distance_list = generate_distance_list()
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()