from mesa import Agent

class Passenger(Agent):
    def __init__(self, unique_id, model, origin, destination):
        super().__init__(unique_id, model)
        self.origin = origin
        self.destination = destination
        self.current_location = origin
        self.on_vehicle = False
        self.travel_time = 0

    def step(self):
        if self.current_location == self.destination:
            print(f"Passenger {self.unique_id} has reached their destination at {self.destination}.")
            
            return

        print(f"Passenger {self.unique_id} at {self.current_location} moving towards {self.destination}.")
        self.travel_time += 1
        if not self.on_vehicle:
            self.move_towards_destination()

    def move_towards_destination(self):
        x, y = self.current_location
        dest_x, dest_y = self.destination
        # Calculer la direction vers la destination
        next_x = x + (1 if dest_x > x else -1 if dest_x < x else 0)
        next_y = y + (1 if dest_y > y else -1 if dest_y < y else 0)

        # Vérifier si la position est valide (dans les limites de la grille)
        if 0 <= next_x < self.model.grid.width and 0 <= next_y < self.model.grid.height:
            if self.model.grid.is_cell_empty((next_x, next_y)):
                self.model.grid.move_agent(self, (next_x, next_y))
                self.current_location = (next_x, next_y)
            else:
                print(f"Cell at {next_x}, {next_y} is occupied, passenger {self.unique_id} can't move there.")
        else:
            print(f"Position {next_x}, {next_y} is out of bounds.")

