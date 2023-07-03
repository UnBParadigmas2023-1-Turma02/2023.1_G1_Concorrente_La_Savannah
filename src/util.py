from mesa.visualization.modules import CanvasGrid, TextElement
from src.agents.gazelle import GazelleAgent
from src.agents.lion import LionAgent
from src.agents.zebra import ZebraAgent


GRID_SIZE = 25

class AgentCountElement(TextElement):
    def render(self, model):
        lion_count = sum(isinstance(agent, LionAgent) for agent in model.schedule.agents)
        gazelle_count = sum(isinstance(agent, GazelleAgent) for agent in model.schedule.agents)
        zebra_count = sum(isinstance(agent, ZebraAgent) for agent in model.schedule.agents)
        return f"Leões: {lion_count} | Gazelas: {gazelle_count} | Zebras: {zebra_count}"


grid_view = CanvasGrid(lambda agent: agent.get_portrayal(), GRID_SIZE, GRID_SIZE, 500, 500)

agent_count = AgentCountElement()