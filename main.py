# Roger Poirier ID: 011110021

from hashTable import HashTable
from package import Package

import csv

def generate_package_Hash_Table(file):
    hash_table = HashTable()
    # Reads packages csv file
    with open(file) as fp:
        reader = csv.DictReader(fp)

        # creates a new package object for each row in csv file
        for row in reader:
            package = Package(row['Package\nID'],row['Address'],row['City '],row['State'],row['Zip'],row['Delivery\nDeadline'],row['Weight\nKILO'])
            hash_table.insert(package.id, package)
        return hash_table

distances = []
with open("distances.csv") as fp:
    reader = csv.DictReader(fp)
    address = next(reader)[:]
    for row in reader:

        distances.append(row)
    print(distances)




# package_table = generate_package_Hash_Table("packages.csv")
# print(package_table.table)
# print(package_table.lookup('5').address)
