from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from model.city_model import CityModel
from agents.passenger import Passenger
from agents.vehicule import Vehicle


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, Passenger):
        # Determine the color based on whether the passenger has reached their destination
        color = "orange" if agent.current_location == agent.destination else "blue"
        portrayal = {
            "Shape": "circle",
            "Color": color,
            "Filled": "true",
            "r": 0.5,
            "Layer": 1,
        }
    elif isinstance(agent, Vehicle):
        # The vehicle becomes red if it's broken down
        color = "red" if agent.broken_down else "green"
        portrayal = {
            "Shape": "rect",
            "Color": color,
            "Filled": "true",
            "w": 0.8,
            "h": 0.8,
            "Layer": 2,
        }
    
    portrayal["x"] = agent.pos[0]
    portrayal["y"] = agent.pos[1]

    return portrayal



grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

perturbation_button = UserSettableParameter("checkbox", "Activate Disturbances", False)

server = ModularServer(
    CityModel,
    [grid],
    "City Simulation",
    {
        "width": UserSettableParameter("slider", "Grid Width", 20, 10, 50, 1),
        "height": UserSettableParameter("slider", "Grid Height", 20, 10, 50, 1),
        "num_passengers": UserSettableParameter("slider", "Number of Passengers", 10, 1, 20, 1),
        "num_vehicles": UserSettableParameter("slider", "Number of Vehicles", 3, 1, 10, 1),
        "perturbation_button": perturbation_button,
    },
)

server.port = 8521
server.launch()
