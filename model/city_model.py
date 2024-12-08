from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import random
from agents.passenger import Passenger
from agents.vehicule import Vehicle

class CityModel(Model):
    def __init__(self, width, height, num_passengers, num_vehicles):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.disturbances = []

        # Create Passengers
        for i in range(num_passengers):
            origin = (random.randint(0, width - 1), random.randint(0, height - 1))
            destination = (random.randint(0, width - 1), random.randint(0, height - 1))
            passenger = Passenger(i, self, origin, destination)
            self.grid.place_agent(passenger, origin)
            self.schedule.add(passenger)

        # Create Vehicles
        for i in range(num_vehicles):
            route = [(x, random.randint(0, height - 1)) for x in range(width)]
            timetable = list(range(len(route)))
            vehicle = Vehicle(i + num_passengers, self, route, timetable)
            self.grid.place_agent(vehicle, route[0])
            self.schedule.add(vehicle)

    def introduce_disturbance(self):
        disturbance_type = random.choice(["roadblock", "breakdown"])
        if disturbance_type == "roadblock":
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            self.disturbances.append(("roadblock", (x, y)))
            print(f"Roadblock introduced at ({x}, {y})")
        elif disturbance_type == "breakdown":
            vehicles = [agent for agent in self.schedule.agents if isinstance(agent, Vehicle)]
            if vehicles:
                vehicle = random.choice(vehicles)
                vehicle.broken_down = True
                print(f"Vehicle {vehicle.unique_id} broke down at {vehicle.pos}")

    def step(self):
        if self.random.random() < 0.1:
            self.introduce_disturbance()
        self.schedule.step()


from mesa import Agent

class Roadblock(Agent):
    def __init__(self, unique_id, model, position):
        super().__init__(unique_id, model)
        self.position = position
