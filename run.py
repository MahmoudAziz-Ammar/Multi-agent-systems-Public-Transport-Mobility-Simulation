from models.city_model import CityModel

# Initialisation du modèle
model = CityModel(10, 10, 3, 5)

# Exécution du modèle pendant 10 étapes
for i in range(10):
    model.step()

# Optionnel: récupère les données
data = model.datacollector.get_agent_vars_dataframe()
print(data)
