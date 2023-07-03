import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

# Importar Agentes
from src.agents.lion import LionAgent
from src.agents.gazelle import GazelleAgent
from src.agents.zebra import ZebraAgent
from src.util import GRID_SIZE


class SavannaModel(Model):
  def __init__(
    self, 
    num_lions = 10, 
    num_gazelles = 10, 
    num_zebras = 10, 
    lion_energy = 25, 
    gazelle_energy = 25, 
    zebra_energy = 25,
    lion_rep_chance = 2,
    zebra_rep_chance = 2,
    gazelle_rep_chance = 2,
    image_checkbox = True,
  ):
    self.grid = MultiGrid(GRID_SIZE, GRID_SIZE, torus=True)
    self.schedule = RandomActivation(self)
    
    self.num_lions = num_lions
    self.num_gazelles = num_gazelles
    self.num_zebras = num_zebras
    self.lion_energy = lion_energy
    self.gazelle_energy = gazelle_energy
    self.zebra_energy = zebra_energy
    self.image_checkbox = image_checkbox
    self.current_id = 0

    for i in range(num_lions):
      x = random.randrange(GRID_SIZE)
      y = random.randrange(GRID_SIZE)
      lion = LionAgent(i, self, lion_energy, lion_rep_chance / 100)
      self.schedule.add(lion)
      self.grid.place_agent(lion, (x, y))
      self.current_id += 1

    for i in range(num_gazelles):
      x = random.randrange(GRID_SIZE)
      y = random.randrange(GRID_SIZE)
      gazelle = GazelleAgent(num_lions + i, self, gazelle_energy, gazelle_rep_chance / 100)
      self.schedule.add(gazelle)
      self.grid.place_agent(gazelle, (x, y))
      self.current_id += 1

    for i in range(num_zebras):
      x = random.randrange(GRID_SIZE)
      y = random.randrange(GRID_SIZE)
      zebra = ZebraAgent(num_lions + num_gazelles + i, self, zebra_energy, zebra_rep_chance / 100)
      self.schedule.add(zebra)
      self.grid.place_agent(zebra, (x, y))
      self.current_id += 1

  def step(self):
    self.schedule.step()
    if self.one_remaining():
      self.running = False

  def one_remaining(self):
    lion_count = sum(isinstance(agent, LionAgent) for agent in self.schedule.agents)
    gazelle_count = sum(isinstance(agent, GazelleAgent) for agent in self.schedule.agents)
    zebra_count = sum(isinstance(agent, ZebraAgent) for agent in self.schedule.agents)
    return (lion_count == 0 and gazelle_count == 0) or (lion_count == 0 and zebra_count == 0) or (gazelle_count == 0 and zebra_count == 0)