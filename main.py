import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from agents import ZebraAgent, GazelleAgent, LionAgent

GRID_SIZE = 25


class AgentCountElement(TextElement):
    def render(self, model):
        lion_count = sum(isinstance(agent, LionAgent) for agent in model.schedule.agents)
        gazelle_count = sum(isinstance(agent, GazelleAgent) for agent in model.schedule.agents)
        zebra_count = sum(isinstance(agent, ZebraAgent) for agent in model.schedule.agents)
        return f"Leões: {lion_count} | Gazelas: {gazelle_count} | Zebras: {zebra_count}"


class SavannaModel(Model):
  def __init__(
    self, 
    num_lions = 10, 
    num_gazelles = 10, 
    num_zebras = 10, 
    lion_energy = 25, 
    gazelle_energy = 25, 
    zebra_energy = 25
  ):
    self.grid = MultiGrid(GRID_SIZE, GRID_SIZE, torus=True)
    self.schedule = RandomActivation(self)
    
    self.num_lions = num_lions
    self.num_gazelles = num_gazelles
    self.num_zebras = num_zebras
    self.lion_energy = lion_energy
    self.gazelle_energy = gazelle_energy
    self.zebra_energy = zebra_energy

    for i in range(num_lions):
      x = random.randrange(GRID_SIZE)
      y = random.randrange(GRID_SIZE)
      lion = LionAgent(i, self, lion_energy)
      self.schedule.add(lion)
      self.grid.place_agent(lion, (x, y))

    for i in range(num_gazelles):
      x = random.randrange(GRID_SIZE)
      y = random.randrange(GRID_SIZE)
      gazelle = GazelleAgent(num_lions + i, self, gazelle_energy)
      self.schedule.add(gazelle)
      self.grid.place_agent(gazelle, (x, y))

    for i in range(num_zebras):
      x = random.randrange(GRID_SIZE)
      y = random.randrange(GRID_SIZE)
      zebra = ZebraAgent(num_lions + num_gazelles + i, self, zebra_energy)
      self.schedule.add(zebra)
      self.grid.place_agent(zebra, (x, y))

  def step(self):
    self.schedule.step()
    if self.one_remaining():
      self.running = False

  def one_remaining(self):
    lion_count = sum(isinstance(agent, LionAgent) for agent in self.schedule.agents)
    gazelle_count = sum(isinstance(agent, GazelleAgent) for agent in self.schedule.agents)
    zebra_count = sum(isinstance(agent, ZebraAgent) for agent in self.schedule.agents)
    return (lion_count == 0 and gazelle_count == 0) or (lion_count == 0 and zebra_count == 0) or (gazelle_count == 0 and zebra_count == 0)


grid_view = CanvasGrid(lambda agent: agent.get_portrayal(), GRID_SIZE, GRID_SIZE, 500, 500)

agent_count = AgentCountElement()

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
    "zebra_energy": Slider("Energia inicial das Zebras", 20, 1, 50)
  }
)

server.port = 8521
server.launch()
