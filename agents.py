import random
from mesa import Agent

class AnimalAgent(Agent):
  def __init__(self, unique_id, model, energy, prey):
    super().__init__(unique_id, model)
    self.energy = energy
    self.prey = prey
    self.str = "Animal"
    self.color = "green"

  def move(self):
    possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    new_position = random.choice(possible_moves)
    self.model.grid.move_agent(self, new_position)
    self.energy -= 1

  def eat(self, prey):
    print(f"== {self.str} comeu {prey.str} ==")
    self.model.grid.remove_agent(prey)
    self.model.schedule.remove(prey)
    self.energy += 5

  def step(self):
    self.move()
    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)
    preys = [agent for agent in neighbors if isinstance(agent, self.prey)]

    if len(preys) > 0:
      prey = random.choice(preys)
      self.eat(prey)

    if self.energy == 0:
      print(f"== {self.str} morreu por falta de energia ==")
      self.model.grid.remove_agent(self)
      self.model.schedule.remove(self)

  def get_portrayal(self):
    return {
      "Shape": "circle", 
      "Color": self.color, 
      "Filled": True, 
      "Layer": 0, 
      "r": 1,
      "text": str(self.energy),
      "text_color": "white",
      "text_position": "bottom"
    }


class GazelleAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy):
    super().__init__(unique_id, model, energy, ZebraAgent)
    self.str = "Gazela"
    self.color = "red"


class LionAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy):
    super().__init__(unique_id, model, energy, GazelleAgent)
    self.str = "Leão"
    self.color = "orange"


class ZebraAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy):
    super().__init__(unique_id, model, energy, LionAgent)
    self.str = "Zebra"
    self.color = "blue"
