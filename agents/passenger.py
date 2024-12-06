from mesa import Agent

class PassengerAgent(Agent):
    """Représente un passager"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.destination = (self.random.randrange(self.model.grid.width), self.random.randrange(self.model.grid.height))

    def move(self):
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
