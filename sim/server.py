from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter


from .agents import Ant, Sugar
from .model import SugarscapeCg

color_dic = {4: "#005C00", 3: "#008300", 2: "#00AA00", 1: "#00F800", 0: "#D6F5D6"}


# number needs to be between 0 and 1.0
def float2hex(number:float) -> str:
    value = int(max(min(number, 1.0), 0.0)*255)
    return f"{value:0{2}x}"

def ant_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Ant:
        rel_vis = agent.vision/6.0
        rel_sugar = agent.sugar/100.0
        portrayal["Color"] = f"#{float2hex(rel_sugar)}00{float2hex(rel_vis)}"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["id/sugar/meta/vis"] = f"{agent.id}/{agent.sugar}/{agent.metabolism}/{agent.vision}"

    elif type(agent) is Sugar:
        portrayal["Color"] = color_dic[agent.amount]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(ant_portrayal, 50, 50, 500, 500)
alive_chart_element = ChartModule([
    {"Label": SugarscapeCg.LIVING_ANTS, "Color": "#00AA00"},
    {"Label": SugarscapeCg.DEAD_ANTS, "Color": "#AA0000"}
])
vision_chart_element = ChartModule([
    {"Label": SugarscapeCg.PERCENT_DEAD_LOW_VISION, "Color": "#000000"},
    {"Label": SugarscapeCg.PERCENT_DEAD_HIGH_VISION, "Color": "#0000FF"}
])

model_params = {
    "initial_population": UserSettableParameter("slider", "Initial Population", 100, 1, 2000, 1),
    "recreate": UserSettableParameter("slider", "Recreate ants every 10 steps", 0, 0, 10, 1),
    "share_knowledge": UserSettableParameter("checkbox", "Share Knowledge", False),
    "solidarity": UserSettableParameter("checkbox", "Solidarity (only with shared knowledge)", False),
}

server = ModularServer(
    SugarscapeCg, [canvas_element, alive_chart_element, vision_chart_element], "Ants", model_params
)
