from mesa import Agent
from agents.passenger import Passenger
import random

class Vehicle(Agent):
    def __init__(self, unique_id, model, route, timetable):
        super().__init__(unique_id, model)
        self.route = route
        self.timetable = timetable
        self.current_stop = 0
        self.broken_down = False
        self.time = 0
        self.passengers = []  # List of passengers currently onboard
        self.pos = route[0]  # Initial position
        self.model.grid.place_agent(self, self.pos)

    def step(self):
        if self.broken_down:
            print(f"Vehicle {self.unique_id} is broken down at {self.pos}")
            return

        # Determine the next stop in the timetable
        self.current_stop = self.timetable[self.time % len(self.timetable)]
        next_location = self.route[self.current_stop]

        # Move toward the next stop cell by cell
        self.move_toward(next_location)

        # Synchronize passenger positions with the vehicle
        for passenger in self.passengers:
            self.model.grid.move_agent(passenger, self.pos)
            passenger.current_location = self.pos
            print(f"Passenger {passenger.unique_id} moved with Vehicle {self.unique_id}")

        self.pick_up_passengers()
        self.time += 1

    def move_toward(self, destination):
        # Calculate the direction from the vehicle's current position to the destination
        x_current, y_current = self.pos
        x_dest, y_dest = destination

        # Move step-by-step toward the destination
        if x_current < x_dest:
            x_current += 1
        elif x_current > x_dest:
            x_current -= 1

        if y_current < y_dest:
            y_current += 1
        elif y_current > y_dest:
            y_current -= 1

        # Update the vehicle's position
        new_pos = (x_current, y_current)

        # If the new position is valid, move the vehicle
        if self.model.grid.is_cell_empty(new_pos):
            self.model.grid.move_agent(self, new_pos)
            self.pos = new_pos
            print(f"Vehicle {self.unique_id} moved to {self.pos}")

    def pick_up_passengers(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=True)
        potential_passengers = []
        for neighbor in neighbors:
            potential_passengers.extend(self.model.grid.get_cell_list_contents([neighbor]))

        passengers_to_pick = [agent for agent in potential_passengers if isinstance(agent, Passenger) and not agent.on_vehicle]

        for passenger in passengers_to_pick:
            self.model.grid.move_agent(passenger, self.pos)
            self.passengers.append(passenger)
            passenger.on_vehicle = True
            print(f"Passenger {passenger.unique_id} picked up by Vehicle {self.unique_id} at {self.pos}")
