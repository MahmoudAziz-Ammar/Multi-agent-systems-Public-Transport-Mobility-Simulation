from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from models.city_model import CityModel
from agents.vehicule_agent import VehicleAgent
from agents.passenger import PassengerAgent

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "r": 1, "Layer": 0}  # Ajoute "Layer"
    if isinstance(agent, VehicleAgent):
        portrayal["Color"] = "blue"
    elif isinstance(agent, PassengerAgent):
        portrayal["Color"] = "green"
    return portrayal

# Créer la grille de visualisation
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Paramètres du modèle
model_params = {
    "width": 10,
    "height": 10,
    "num_vehicles": 3,
    "num_passengers": 5
}

# Créer le serveur
server = ModularServer(CityModel, [grid], "Public Transport Simulation", model_params)

# Lancer le serveur
server.port = 8520
server.launch()
