from src.agents.animalAgent import AnimalAgent

class GazelleAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy, rep_chance):
    super().__init__(unique_id, model, energy, rep_chance, AnimalAgent)
    self.str = "Gazela"
    self.color = "red"
    self.shape = "src/assets/gazelle.png"
    self.prey = "Leão"
    self.name = "Gazelle"