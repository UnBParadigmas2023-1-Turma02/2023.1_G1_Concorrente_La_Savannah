from src.agents.animalAgent import AnimalAgent

class ZebraAgent(AnimalAgent):
  def __init__(self, unique_id, model, energy, rep_chance):
    super().__init__(unique_id, model, energy, rep_chance, AnimalAgent)
    self.str = "Zebra"
    self.color = "blue"
    self.shape = "src/assets/zebra.png"
    self.prey = "Gazela"
    self.name = "Zebra"