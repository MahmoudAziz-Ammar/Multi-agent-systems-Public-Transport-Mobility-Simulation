from mesa import Agent
from agents.passenger import Passenger


class Vehicle(Agent):
    def __init__(self, unique_id, model, route, timetable):
        super().__init__(unique_id, model)
        self.route = route
        self.timetable = timetable
        self.current_stop = 0
        self.broken_down = False

    def step(self):
        if self.broken_down:
            print(f"Vehicle {self.unique_id} is broken down at {self.pos}")
            return

        self.current_stop = (self.current_stop + 1) % len(self.route)
        next_location = self.route[self.current_stop]

        if self.model.grid.is_cell_empty(next_location):
            self.model.grid.move_agent(self, next_location)
            print(f"Vehicle {self.unique_id} moved to {next_location}")

        self.pick_up_passengers()

    def pick_up_passengers(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        passengers_to_pick = [agent for agent in cellmates if isinstance(agent, Passenger)]
    
        if not passengers_to_pick:
            print(f"Vehicle {self.unique_id} found no passengers to pick up at {self.pos}")
    
        for passenger in passengers_to_pick:
            print(f"Vehicle {self.unique_id} picked up Passenger {passenger.unique_id}")
            self.model.grid.remove_agent(passenger)
            self.model.schedule.remove(passenger)
