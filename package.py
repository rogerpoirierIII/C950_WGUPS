from inspect import EndOfBlock


class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight,special_note = None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note

    # def __str__(self):
    #     return "%s, %s, %s, %s, %s, %s, %s" % (
    #         self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight,
    #         )
