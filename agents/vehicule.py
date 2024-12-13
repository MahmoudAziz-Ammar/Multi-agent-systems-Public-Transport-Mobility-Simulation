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
        self.passengers = []  # Liste des passagers à bord
        self.pos = route[0]  # Position initiale
        self.model.grid.place_agent(self, self.pos)

    def step(self):
        if self.broken_down:
            print(f"Vehicle {self.unique_id} is broken down at {self.pos}")
            return

        # Déposer les passagers qui ont atteint leur destination
        self.drop_passengers()

        # Si le véhicule a des passagers, se rendre vers la destination du premier passager
        if self.passengers:
            self.travel_to_passenger_destination()
        else:
            # Si aucun passager, se déplacer selon l'itinéraire normal
            self.move_to_next_stop()

        # Synchroniser la position du véhicule et des passagers
        for passenger in self.passengers:
            self.model.grid.move_agent(passenger, self.pos)
            passenger.current_location = self.pos
            print(f"Passenger {passenger.unique_id} moved with Vehicle {self.unique_id}")

        # Prendre de nouveaux passagers
        self.pick_up_passengers()

        self.time += 1

    def move_to_next_stop(self):
        """Déplacer le véhicule à l'arrêt suivant sur son itinéraire."""
        if self.current_stop < len(self.route) - 1:
            self.current_stop += 1
        self.move_toward(self.route[self.current_stop])

    def travel_to_passenger_destination(self):
        """Se déplacer vers la destination du premier passager à bord."""
        passenger = self.passengers[0]
        destination = passenger.destination
        self.move_toward(destination)

        # Si le véhicule arrive à la destination du passager, déposer le passager
        if self.pos == destination:
            self.drop_passenger(passenger)

    def move_toward(self, destination):
        """Déplacer le véhicule vers une destination."""
        x_current, y_current = self.pos
        x_dest, y_dest = destination

        # Déplacer le véhicule vers la destination de manière graduelle
        if x_current < x_dest:
            x_current += 1
        elif x_current > x_dest:
            x_current -= 1

        if y_current < y_dest:
            y_current += 1
        elif y_current > y_dest:
            y_current -= 1

        new_pos = (x_current, y_current)

        # Si la position est valide, déplacer le véhicule
        if self.model.grid.is_cell_empty(new_pos):
            self.model.grid.move_agent(self, new_pos)
            self.pos = new_pos
            print(f"Vehicle {self.unique_id} moved to {self.pos}")

    def pick_up_passengers(self):
        """Prendre les passagers à proximité du véhicule."""
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=True)
        potential_passengers = []
        for neighbor in neighbors:
            potential_passengers.extend(self.model.grid.get_cell_list_contents([neighbor]))

        passengers_to_pick = [agent for agent in potential_passengers if isinstance(agent, Passenger) and not agent.on_vehicle]

        for passenger in passengers_to_pick:
            if not passenger.reached_destination:  # Correction de la faute de frappe
                self.model.grid.move_agent(passenger, self.pos)
                self.passengers.append(passenger)
                passenger.on_vehicle = True
                print(f"Passenger {passenger.unique_id} picked up by Vehicle {self.unique_id} at {self.pos}")

    def drop_passenger(self, passenger):
        """Déposer un passager à sa destination."""
        self.passengers.remove(passenger)
        passenger.on_vehicle = False
        passenger.reached_destination=True
        self.model.grid.move_agent(passenger, passenger.destination)
        print(f"Passenger {passenger.unique_id} dropped off by Vehicle {self.unique_id} at {passenger.destination}")

    def drop_passengers(self):
        """Déposer tous les passagers arrivés à leur destination."""
        passengers_to_drop = [passenger for passenger in self.passengers if passenger.destination == self.pos]
        for passenger in passengers_to_drop:
            self.drop_passenger(passenger)
