from src.agents.animalAgent import AnimalAgent

class LionAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy, rep_chance):
    super().__init__(unique_id, model, energy, rep_chance, AnimalAgent)
    self.str = "Leão"
    self.color = "orange"
    self.shape = "src/assets/lion.png"
    self.prey = "Zebra"