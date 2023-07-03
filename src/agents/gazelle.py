from src.agents.animalAgent import AnimalAgent

class GazelleAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy, rep_chance, image):
    super().__init__(unique_id, model, energy, rep_chance, image, AnimalAgent)
    self.str = "Gazela"
    self.color = "brown"
    self.shape = "src/assets/gazelle.png"
    self.prey = "Leão"
    self.name = "Gazelle"
    self.image = image
    self.text_color = "white"