from mesa import Agent

class Passenger(Agent):
    def __init__(self, unique_id, model, origin, destination, reached_destination=False):
        super().__init__(unique_id, model)
        self.origin = origin
        self.destination = destination
        self.current_location = origin
        self.on_vehicle = False
        self.travel_time = 0
        self.reached_destination = reached_destination  # Correction de la faute de frappe

    def step(self):
        if self.current_location == self.destination:
            print(f"Passenger {self.unique_id} has reached their destination at {self.destination}.")
            print(f"Total travel time for Passenger {self.unique_id} is : {self.travel_time} steps.")
            self.reached_destination = True  # Correction de la faute de frappe
            return

        self.travel_time += 1

        if not self.on_vehicle:
            self.move_towards_vehicle()
        else:
            # Passenger is on a vehicle, move with the vehicle
            pass

    def move_towards_vehicle(self):
        x, y = self.current_location
        dest_x, dest_y = self.destination
        next_x = x + (1 if dest_x > x else -1 if dest_x < x else 0)
        next_y = y + (1 if dest_y > y else -1 if dest_y < y else 0)

        if 0 <= next_x < self.model.grid.width and 0 <= next_y < self.model.grid.height:
            if self.model.grid.is_cell_empty((next_x, next_y)):
                self.model.grid.move_agent(self, (next_x, next_y))
                self.current_location = (next_x, next_y)
                print(f"Passenger {self.unique_id} moved to {self.current_location}")
            else:
                print(f"Cell at {next_x}, {next_y} is occupied, passenger {self.unique_id} can't move there.")

    def board_vehicle(self, vehicle):
        # Check if the passenger is at the vehicle's stop and can board
        if self.current_location == vehicle.pos and not self.on_vehicle:
            self.on_vehicle = True
            vehicle.passengers.append(self)  # Add passenger to the vehicle
            print(f"Passenger {self.unique_id} boarded Vehicle {vehicle.unique_id} at {self.current_location}")

    def drop_off(self, vehicle):
        # If the passenger's destination is reached, drop them off
        if self.current_location == self.destination and self.on_vehicle:
            vehicle.passengers.remove(self)  # Remove from vehicle
            self.on_vehicle = False
            self.reached_destination = True
            print(f"Passenger {self.unique_id} dropped off by Vehicle {vehicle.unique_id} at {self.current_location}")
