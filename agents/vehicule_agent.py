from mesa import Agent

from mesa import Agent

class VehicleAgent(Agent):
    """Représente un véhicule de transport public"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        x, y = self.pos
        self.model.grid.move_agent(self, (self.random.randrange(self.model.grid.width), self.random.randrange(self.model.grid.height)))

    def step(self):
        self.move()
