# Roger Poirier ID: 011110021

from hashTable import HashTable
from package import Package

import csv

package_hash = HashTable()
with open("packages.csv", encoding="utf-8") as fp:
    reader = csv.DictReader(fp,delimiter=",")

    for row in reader:

        # create a Package instance to store in the hash table
        package = Package(row['Package\nID'],row['Address'],row['City '],row['State'],row['Zip'],row['Delivery\nDeadline'],row['Weight\nKILO'])

        package_hash.insert(package.id, package)

    print(package_hash.table)
    print(package_hash.lookup('5').address)