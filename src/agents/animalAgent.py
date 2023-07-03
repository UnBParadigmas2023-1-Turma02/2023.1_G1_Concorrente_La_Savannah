import random
from mesa import Agent

class AnimalAgent(Agent):
  def __init__(self, unique_id, model, energy, rep_percentage, image, prey):
    super().__init__(unique_id, model)
    self.energy = energy
    self.prey = prey
    self.str = "Animal"
    self.color = "green"
    self.rep_percentage = rep_percentage
    self.shape = "circle"
    self.image = image

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

  def reproduce(self):
    if self.pos and random.random() < self.rep_percentage:
      empty_cells = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=1)
      empty_cells = [cell for cell in empty_cells if self.model.grid.is_cell_empty(cell)]
      if empty_cells:
        print(f"== {self.str} reproduziu ==")
        x, y = random.choice(empty_cells)
        new_agent = type(self)(self.model.next_id(), self.model, self.energy, self.rep_percentage, self.image)
        self.model.schedule.add(new_agent)
        self.model.grid.place_agent(new_agent, (x, y))
        self.model.current_id += 1

  def step(self):
    self.move()
    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)
    preys = [agent for agent in neighbors if (agent.str == self.prey)]

    if len(preys) > 0:
      prey = random.choice(preys)
      self.eat(prey)

    if self.energy == 0:
      print(f"== {self.str} morreu por falta de energia ==")
      self.model.grid.remove_agent(self)
      self.model.schedule.remove(self)
    
    self.reproduce()

  def get_portrayal(self):
    if self.image == False:
      return {
        "Shape": "circle", 
        "Color": self.color, 
        "Filled": True, 
        "Layer": 0, 
        "r": 1,
        "text": str(self.energy),
        "text_color": self.text_color,
        "text_position": "bottom"
      }
    else:
      if self.energy > 10:
        image = "src/assets/Green_" + self.name + ".png"
      elif self.energy > 5 and self.energy < 10:
        image = "src/assets/Yellow_" + self.name + ".png"
      else: 
        image = "src/assets/Red_" + self.name + ".png"
      return {
        "Shape": image,
        "Layer": 0,
        "scale": 1.5, 
      }