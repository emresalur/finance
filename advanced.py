from setupadvanced import *
from mesa.visualization.ModularVisualization import VisualizationElement, CHART_JS_FILE
import mesa
import numpy as np

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    
    if agent.wealth > 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = mesa.visualization.ChartModule([{"Label": "Gini", "Color": "Black"}], data_collector_name='datacollector')

class HistogramModule(VisualizationElement):
    package_includes = [CHART_JS_FILE]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wealth_vals = [agent.wealth for agent in model.schedule.agents]
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        return [int(x) for x in hist]

# Create a histogram to display the wealth distribution
hist = HistogramModule(list(range(10)), 200, 500)

server = mesa.visualization.ModularServer(MoneyModel, 
    [grid, chart], 
    "Money Model", 
    {"N": 100, "width": 10, "height": 10}
)

server.launch()
