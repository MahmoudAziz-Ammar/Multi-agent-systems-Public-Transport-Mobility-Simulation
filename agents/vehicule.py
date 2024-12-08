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
        # Make sure the vehicle is placed on the grid
        self.pos = route[0]  # Initial position
        self.model.grid.place_agent(self, self.pos)

    def step(self):
        if self.broken_down:
            print(f"Vehicle {self.unique_id} is broken down at {self.pos}")
            return

        # Introduce a random perturbation (e.g., breakdown) at each step
        self.introduce_perturbation()

        self.current_stop = (self.current_stop + 1) % len(self.route)
        next_location = self.route[self.current_stop]

        if self.model.grid.is_cell_empty(next_location):
            self.model.grid.move_agent(self, next_location)
            print(f"Vehicle {self.unique_id} moved to {next_location}")

        # Attempt to pick up passengers after moving
        self.pick_up_passengers()

    def pick_up_passengers(self):
        # Get the neighboring cells (including the vehicle's current cell)
        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=True
        )

        # Get all agents in the neighboring cells
        potential_passengers = []
        for neighbor in neighbors:
            potential_passengers.extend(self.model.grid.get_cell_list_contents([neighbor]))

        # Filter only Passenger agents
        passengers_to_pick = [agent for agent in potential_passengers if isinstance(agent, Passenger)]

        if not passengers_to_pick:
            print(f"Vehicle {self.unique_id} found no passengers to pick up at {self.pos}")
            return

        # Handle the passengers
        for passenger in passengers_to_pick:
            print(f"Vehicle {self.unique_id} picked up Passenger {passenger.unique_id}")
            
            # Ensure the passenger is in the grid before removing
            if passenger in self.model.grid.get_cell_list_contents([self.pos]):
                try:
                    self.model.grid.remove_agent(passenger)
                    self.model.schedule.remove(passenger)
                except Exception as e:
                    print(f"Error while picking up Passenger {passenger.unique_id}: {e}")
            else:
                print(f"Warning: Passenger {passenger.unique_id} not in vehicle's current position.")

    def introduce_perturbation(self):
        # Randomly decide if a perturbation should occur
        if random.random() < 0.1:  # 10% chance for a perturbation
            perturbation_type = random.choice(['breakdown', 'delay', 'route_change'])

            if perturbation_type == 'breakdown':
                self.broken_down = True
                print(f"Vehicle {self.unique_id} has broken down at {self.pos}.")

            elif perturbation_type == 'delay':
                delay_time = random.randint(1, 3)  # Random delay between 1 and 3 steps
                print(f"Vehicle {self.unique_id} has been delayed by {delay_time} steps.")

            elif perturbation_type == 'route_change':
                new_route_index = random.randint(0, len(self.route) - 1)
                self.route = self.route[new_route_index:] + self.route[:new_route_index]
                print(f"Vehicle {self.unique_id} has changed its route. New route: {self.route}")

