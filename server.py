from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from model.city_model import CityModel
from mesa  import Agent

from agents.passenger import Passenger
from agents.vehicule import Vehicle

class Roadblock(Agent):
    def __init__(self, unique_id, model, position):
        super().__init__(unique_id, model)
        self.position = position






def agent_portrayal(agent):
    if isinstance(agent, Passenger):
        return {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "r": 0.5,
            "Layer": 1,
        }
    elif isinstance(agent, Vehicle):
        color = "red" if agent.broken_down else "transparent"  # Rouge si panne
        return {
            "Shape": "bus.png",  # Chemin vers l'image
            "Color": color,  # Change la couleur de fond
            "Filled": "true",
            "w": 0.8,
            "h": 0.8,
            "Layer": 2,
        }
    elif isinstance(agent, Roadblock):
        return {
            "Shape": "rect",
            "Color": "black",
            "Filled": "true",
            "w": 0.8,
            "h": 0.8,
            "Layer": 0,
        }
    return {}




grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

server = ModularServer(
    CityModel,
    [grid],
    "City Simulation",
    {
        "width": UserSettableParameter("slider", "Grid Width", 20, 10, 50, 1),
        "height": UserSettableParameter("slider", "Grid Height", 20, 10, 50, 1),
        "num_passengers": UserSettableParameter("slider", "Number of Passengers", 10, 1, 20, 1),
        "num_vehicles": UserSettableParameter("slider", "Number of Vehicles", 3, 1, 10, 1),
    },
)

