class Flight():
    def __init__(self, capacity):  # init creates a new flight
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, name): # add_passenger adds a new passenger to a flight
        if not self.open_seats():
            return False
        self.passengers.append(name)
        return True

    def open_seats(self): # open_seats tells us how many open seats there are
        return self.capacity - len(self.passengers)


flight = Flight(3)

people = ["Harry", "Ron", "Hermione", "Ginny"]
for person in people:
    success = flight.add_passenger(person)
    if success:
        print(f"Added {person} to the flight successfully.")
    else:
        print(f"No available seats for {person}.")