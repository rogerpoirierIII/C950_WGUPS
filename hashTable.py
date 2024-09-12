class HashTable:
    def __init__(self, capacity=10):
    # Initializes the hash table with the given capacity.
        self.capacity = capacity
        self.table = [None] * capacity
    # Counter for the number of elements in the hash table.
        self.size = 0

    # Returns length of the hash table.
        def __len__(self):
            return self.size
    # Returns the hash value for a given key.
    def _hash(self, key):
        return hash(key)
    # Inserts the given key-value pair into the hash table.
    def insert(self, key, value):

    # Creates index for the given key.
        index = self._hash(key) % self.capacity
    # Checks if the bucket is empty. If empty, inserts the key-value pair.
        if self.table[index] is None:
            self.table[index] = [(key, value)]
    # If the bucket is not empty, appends the key-value pair to the list.
        else:
            self.table[index].append((key, value))
    # Increments the size of the hash table.
        self.size += 1
    # Doubles the capacity of the table if the load factor is greater or equal to 0.7
        if self.size / self.capacity >= 0.7:
            self._resize(self.capacity * 2)

    # Searches for the given key in the hash table.
    # Checks at the index of the given key. If the key is found, returns the value.
    # If the key is not found, returns None.
    def lookup(self, key):
        index = self._hash(key) % self.capacity
        if self.table[index] is not None:
            for ID, package in self.table[index]:
                if ID == key:
                    return package
        return None

    # Creates a new hash table with the given new capacity.
    # After the table is created, rehashes all the key-value pairs to the new table.
    def _resize(self, new_capacity):
        old_table = self.table
        self.capacity = new_capacity
        self.table = [None] * self.capacity
        self.size = 0
        for bucket in old_table:
            if bucket is not None:
                for key, value in bucket:
                    self.insert(key, value)

    def print(self):
        print(self.table)

