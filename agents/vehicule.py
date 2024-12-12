from mesa import Agent
from agents.passenger import Passenger

import random

from mesa import Agent

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

        self.current_stop = self.timetable[self.time % len(self.timetable)]
        next_location = self.route[self.current_stop]

        if self.model.grid.is_cell_empty(next_location):
            self.model.grid.move_agent(self, next_location)
            self.pos = next_location
            print(f"Vehicle {self.unique_id} moved to {next_location}")

        # Synchronize passenger positions with the vehicle
        for passenger in self.passengers:
            self.model.grid.move_agent(passenger, self.pos)
            passenger.current_location = self.pos
            print(f"Passenger {passenger.unique_id} moved with Vehicle {self.unique_id}")

        self.pick_up_passengers()
        self.time += 1

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



 

