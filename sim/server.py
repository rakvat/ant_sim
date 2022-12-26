from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import Checkbox, Slider


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
        rel_vis = agent.senses/6.0
        rel_sugar = agent.sugar/100.0
        portrayal["Color"] = f"#FFFF00" if agent.individualist else f"#{float2hex(rel_sugar)}00{float2hex(rel_vis)}"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["id/sugar/meta/vis"] = f"{agent.id}/{agent.sugar}/{agent.metabolism}/{agent.senses}"

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
senses_chart_element = ChartModule([
    {"Label": SugarscapeCg.PERCENT_DEAD_LOW_SENSES, "Color": "#000000"},
    {"Label": SugarscapeCg.PERCENT_DEAD_HIGH_SENSES, "Color": "#0000FF"},
    {"Label": SugarscapeCg.PERCENT_DEAD_INDIVIDUALISTS, "Color": "#FFFF00"},
])

model_params = {
    "initial_population": Slider("Initial Population", value=100, min_value=2, max_value=2000, step=1),
    "recreate": Slider("Recreate ants every 10 steps", value=0, min_value=0, max_value=10, step=1),
    "shared_knowledge": Checkbox("Shared Knowledge", False),
    "solidarity": Checkbox("Solidarity", False),
    "individualist_percent": Slider("Percent individualists", value=0, min_value=0, max_value=100, step=1, description="only with solidarity"),
}

server = ModularServer(
    SugarscapeCg, [canvas_element, alive_chart_element, senses_chart_element], "Ants", model_params
)
