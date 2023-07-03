import random

from mesa import Agent


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