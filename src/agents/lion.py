from src.agents.animalAgent import AnimalAgent

class LionAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy, rep_chance, image):
    super().__init__(unique_id, model, energy, rep_chance, image, AnimalAgent)
    self.str = "Leão"
    self.color = "orange"
    self.shape = "src/assets/lion.png"
    self.prey = "Zebra"
    self.name = "Lion"
    self.image = image
    self.text_color = "brown"