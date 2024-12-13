from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import random
from agents.passenger import Passenger
from agents.vehicule import Vehicle
from mesa import Agent

class CityModel(Model):
    def __init__(self, width, height, num_passengers, num_vehicles,perturbation_button):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.disturbances = []
        self.perturbation_button = perturbation_button


        if self.perturbation_button:
            self.activate_perturbations()

        # Create Passengers
        for i in range(num_passengers):
            origin = (random.randint(0, width - 1), random.randint(0, height - 1))
            destination = (random.randint(0, width - 1), random.randint(0, height - 1))
            passenger = Passenger(i, self, origin, destination,reached_destination=False)
            self.grid.place_agent(passenger, origin)
            self.schedule.add(passenger)

        # Create Vehicles
        for i in range(num_vehicles):
            route = [(x, random.randint(0, height - 1)) for x in range(width)]
            timetable = list(range(len(route)))
            vehicle = Vehicle(i + num_passengers, self, route, timetable)
            self.grid.place_agent(vehicle, route[0])
            self.schedule.add(vehicle)

    


    def activate_perturbations(self):
        disturbance_type = random.choice(["roadblock", "breakdown"])
        print("i think we have : "+disturbance_type)
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
        # Afficher que la méthode step est appelée
        print("Step called")

        # Afficher les positions des passagers
        print("Positions of all passengers:")
        count = 0
        for agent in self.schedule.agents:
            if isinstance(agent, Passenger):
                print(f"Passenger {agent.unique_id} at {agent.current_location} moving towards {agent.destination}")
                count += 1
                if count >= 5:  # Limiter l'affichage à 5 passagers pour éviter trop d'informations
                    break

        # Vérification de la cohérence entre les agents et la grille
        if isinstance(self.schedule.agents, dict):
            agents = self.schedule.agents.values()
        elif isinstance(self.schedule.agents, list):
            agents = self.schedule.agents
        else:
            raise TypeError("Unexpected type for schedule.agents")

        for agent in agents:
            if agent not in self.grid.get_cell_list_contents(agent.pos):
                print(f"Warning: Agent {agent.unique_id} is not synchronized between schedule and grid.")

        # Introduire une perturbation de temps en temps
        if self.random.random() < 0.1:
            self.activate_perturbations()

        # Effectuer un pas dans le temps pour tous les agents
        self.schedule.step()

  




class Roadblock(Agent):
    def __init__(self, unique_id, model, position):
        super().__init__(unique_id, model)
        self.position = position
