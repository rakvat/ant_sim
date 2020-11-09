"""
Sugarscape Constant Growback Model
================================

Replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
"""

import numpy as np
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import Ant, Sugar
from .schedule import RandomActivationByBreed


class SugarscapeCg(Model):
    """
    Sugarscape 2 Constant Growback
    """

    LIVING_ANTS = "Living Ants"
    DEAD_ANTS = "Dead Ants"
    PERCENT_DEAD_LOW_VISION = "% Dead Low Vision"
    PERCENT_DEAD_HIGH_VISION = "% Dead High Vision"

    verbose = True  # Print-monitoring

    def __init__(self, height=50, width=50, initial_population=100):
        """
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        """

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = initial_population

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector({
            self.LIVING_ANTS: lambda m: m.schedule.get_breed_count(Ant),
            self.DEAD_ANTS: lambda m: m.schedule.num_dead,
            self.PERCENT_DEAD_LOW_VISION: lambda m: m.schedule.percent_dead(low_vision=True),
            self.PERCENT_DEAD_HIGH_VISION: lambda m: m.schedule.percent_dead(low_vision=False),
        })

        # Create sugar
        sugar_distribution = np.genfromtxt("sim/sugar-map.txt")
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create ants:
        for i in range(self.initial_population):
            sugar = self.random.randrange(6, 25)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            while self.is_occupied(pos:=(
                self.random.randrange(self.width),
                self.random.randrange(self.height)
            )):
                pass

            ant = Ant(pos, self, False, sugar, metabolism, vision)
            self.grid.place_agent(ant, pos)
            self.schedule.add(ant)

        self.running = True
        self.datacollector.collect(self)

    def is_occupied(self, pos):
        this_cell = self.grid.get_cell_list_contents([pos])
        return len(this_cell) > 1

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time, self.schedule.get_breed_count(Ant)])

    def run_model(self, step_count=200):

        if self.verbose:
            print(
                "Initial number Sugarscape Agent: ",
                self.schedule.get_breed_count(Ant),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print(
                "Final number Sugarscape Agent: ",
                self.schedule.get_breed_count(Ant),
            )
