from src.agents.animalAgent import AnimalAgent

class ZebraAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy, rep_chance, image):
    super().__init__(unique_id, model, energy, rep_chance, image, AnimalAgent)
    self.str = "Zebra"
    self.color = "black"
    self.shape = "src/assets/zebra.png"
    self.prey = "Gazela"
    self.name = "Zebra"
    self.image = image
    self.text_color = "white"