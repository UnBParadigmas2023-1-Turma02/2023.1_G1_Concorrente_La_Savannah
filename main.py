import random
from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

GRID_SIZE = 25

def agent_portrayal(agent):
  if isinstance(agent, LionAgent):
    return {
      "Shape": "circle", 
      "Color": "orange", 
      "Filled": True, 
      "Layer": 0, 
      "r": 1,
      "text": str(agent.energy),
      "text_color": "white",
      "text_position": "bottom"
    }
  elif isinstance(agent, GazelleAgent):
    return {
      "Shape": "circle", 
      "Color": "red", 
      "Filled": True, 
      "Layer": 0, 
      "r": 1,
      "text": str(agent.energy),
      "text_color": "white",
      "text_position": "bottom"
    } 

  elif isinstance(agent, ZebraAgent):
    return {
      "Shape": "circle", 
      "Color": "blue", 
      "Filled": True, 
      "Layer": 0, 
      "r": 1,
      "text": str(agent.energy),
      "text_color": "white",
      "text_position": "bottom"
    } 

class AgentCountElement(TextElement):
    def render(self, model):
        lion_count = sum(isinstance(agent, LionAgent) for agent in model.schedule.agents)
        gazelle_count = sum(isinstance(agent, GazelleAgent) for agent in model.schedule.agents)
        zebra_count = sum(isinstance(agent, ZebraAgent) for agent in model.schedule.agents)
        return f"Leões: {lion_count} | Gazelas: {gazelle_count} | Zebras: {zebra_count}"

class SavannaModel(Model):
  def __init__(self, num_lions = 10, num_gazelles = 10, num_zebras = 10, lion_energy = 25, gazelle_energy = 25, zebra_energy = 25):
    self.grid = MultiGrid(GRID_SIZE, GRID_SIZE, torus=True)
    self.schedule = RandomActivation(self)

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

class LionAgent(Agent):
  def __init__(self, unique_id, model, lion_energy):
    super().__init__(unique_id, model)
    self.energy = lion_energy

  def move(self):
    possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    new_position = random.choice(possible_moves)
    self.model.grid.move_agent(self, new_position)
    self.energy -= 1

  def eat(self, prey):
    print("== Leão comeu Gazela ==")
    self.model.grid.remove_agent(prey)
    self.model.schedule.remove(prey)
    self.energy += 5

  def step(self):
    self.move()
    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)
    gazelles = [agent for agent in neighbors if isinstance(agent, GazelleAgent)]
    if len(gazelles) > 0:
      prey = random.choice(gazelles)
      self.eat(prey)

    if self.energy == 0:
      self.model.grid.remove_agent(self)
      self.model.schedule.remove(self)

class GazelleAgent(Agent):
  def __init__(self, unique_id, model, gazelle_energy):
    super().__init__(unique_id, model)
    self.energy = gazelle_energy

  def move(self):
    possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    new_position = random.choice(possible_moves)
    self.model.grid.move_agent(self, new_position)
    self.energy -= 1

  def eat(self, prey):
    print("== Gazelle comeu Zebra ==")
    self.model.grid.remove_agent(prey)
    self.model.schedule.remove(prey)
    self.energy += 5

  def step(self):
    self.move()
    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)
    zebras = [agent for agent in neighbors if isinstance(agent, ZebraAgent)]
    if len(zebras) > 0:
      prey = random.choice(zebras)
      self.eat(prey)

    if self.energy == 0:
      print("== Gazela morreu por falta de energia ==")
      self.model.grid.remove_agent(self)
      self.model.schedule.remove(self)

class ZebraAgent(Agent):
  def __init__(self, unique_id, model, zebra_energy):
    super().__init__(unique_id, model)
    self.energy = zebra_energy
    
  def move(self):
    possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    new_position = random.choice(possible_moves)
    self.model.grid.move_agent(self, new_position)
    self.energy -= 1

  def eat(self, prey):
    print("== Zebra comeu Leão ==")
    self.model.grid.remove_agent(prey)
    self.model.schedule.remove(prey)
    self.energy += 5

  def step(self):
    self.move()
    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)
    lions = [agent for agent in neighbors if isinstance(agent, LionAgent)]
    if len(lions):
      prey = random.choice(lions)
      self.eat(prey)
  
    if self.energy == 0:
      self.model.grid.remove_agent(self)
      self.model.schedule.remove(self)

grid_view = CanvasGrid(agent_portrayal, GRID_SIZE, GRID_SIZE, 500, 500)

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
