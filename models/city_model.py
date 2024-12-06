from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class CityModel(Model):
    def __init__(self, width, height, num_vehicles, num_passengers):
        self.num_agents = num_vehicles + num_passengers
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        # Crée les véhicules
        for i in range(num_vehicles):
            a = VehicleAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
        # Crée les passagers
        for i in range(num_passengers):
            a = PassengerAgent(i + num_vehicles, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
        # Data collection
        self.datacollector = DataCollector(agent_reporters={"Passenger Locations": "pos"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

class VehicleAgent(Agent):
    """Un agent représentant un véhicule de transport public"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        # Exemple simple: mouvement aléatoire pour un véhicule
        x, y = self.pos
        self.model.grid.move_agent(self, (self.random.randrange(self.model.grid.width), self.random.randrange(self.model.grid.height)))

    def step(self):
        self.move()

class PassengerAgent(Agent):
    """Un agent représentant un passager"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.destination = (self.random.randrange(self.model.grid.width), self.random.randrange(self.model.grid.height))

    def move(self):
        # Exemple simple: se déplacer vers la destination
        x, y = self.pos
        dest_x, dest_y = self.destination
        if x < dest_x:
            x += 1
        elif x > dest_x:
            x -= 1
        if y < dest_y:
            y += 1
        elif y > dest_y:
            y -= 1
        self.model.grid.move_agent(self, (x, y))

    def step(self):
        self.move()
