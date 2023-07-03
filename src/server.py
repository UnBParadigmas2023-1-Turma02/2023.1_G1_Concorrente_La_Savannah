import mesa
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from src.savanna import SavannaModel
from src.util import grid_view, agent_count

server = ModularServer(
  SavannaModel, 
  [grid_view, agent_count], 
  "Savanna Model", 
  {
    "num_lions": Slider("Quantidade de Leões", 10, 1, 50),
    "num_gazelles": Slider("Quantidade de Gazelas", 10, 1, 50),
    "num_zebras": Slider("Quantidade de Zebras", 10, 1, 50),
    "lion_energy": Slider("Energia inicial dos Leões", 20, 1, 50),
    "gazelle_energy": Slider("Energia inicial das Gazelas", 20, 1, 50),
    "zebra_energy": Slider("Energia inicial das Zebras", 20, 1, 50),
    "lion_rep_chance": Slider("Chance de reprodução do Leão", 2, 1, 100),
    "zebra_rep_chance": Slider("Chance de reprodução da Zebra", 2, 1, 100),
    "gazelle_rep_chance": Slider("Chance de reprodução do Gazela", 2, 1, 100)
  },
  8521
)