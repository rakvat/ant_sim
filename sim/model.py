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
from .shared_knowledge import SharedKnowledge
from .distribution import Distribution


class SugarscapeCg(Model):
    """
    Sugarscape 2 Constant Growback
    """

    LIVING_ANTS = "Living Ants"
    DEAD_ANTS = "Dead Ants"
    PERCENT_DEAD_LOW_SENSES = "% Dead Low Senses"
    PERCENT_DEAD_HIGH_SENSES = "% Dead High Senses"
    PERCENT_DEAD_INDIVIDUALISTS = "% Dead Individualist"

    verbose = True  # Print-monitoring

    def __init__(self, height=50, width=50, initial_population=100, recreate=0, shared_knowledge=False, solidarity=False, individualist_percent=0):
        """
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        """

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = initial_population
        self.recreate = recreate

        self.schedule = RandomActivationByBreed(self)
        self.shared_knowledge = SharedKnowledge(width=width, height=height) if shared_knowledge else None
        self.distribution = Distribution() if solidarity else None
        self.solidarity = solidarity
        self.individualist_percent = individualist_percent if self.solidarity else 0

        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector({
            "initial_population": lambda m: m.initial_population,
            "shared_knowledge": lambda m: m.shared_knowledge is not None,
            "recreate": lambda m: m.recreate,
            "solidarity": lambda m: m.solidarity,
            "individualist_percent": lambda m: m.individualist_percent,
            self.LIVING_ANTS: lambda m: m.schedule.get_breed_count(Ant),
            self.DEAD_ANTS: lambda m: m.schedule.num_dead,
            self.PERCENT_DEAD_LOW_SENSES: lambda m: m.schedule.percent_dead(filter=self.PERCENT_DEAD_LOW_SENSES),
            self.PERCENT_DEAD_HIGH_SENSES: lambda m: m.schedule.percent_dead(filter=self.PERCENT_DEAD_HIGH_SENSES),
            self.PERCENT_DEAD_INDIVIDUALISTS: lambda m: m.schedule.percent_dead(filter=self.PERCENT_DEAD_INDIVIDUALISTS),
            "min_sugar": lambda m: m.schedule.min_sugar(),
            "max_sugar": lambda m: m.schedule.max_sugar(),
            "avg_sugar": lambda m: m.schedule.avg_sugar(),
            "stdev_sugar": lambda m: m.schedule.stdev_sugar(),
        })

        # Create sugar
        sugar_distribution = np.genfromtxt("sim/sugar-map.txt")
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create ants:
        for _ in range(self.initial_population):
            self._create_ant()

        self.running = True
        self.datacollector.collect(self)

    def _create_ant(self):
        sugar = self.random.randrange(6, 25)
        metabolism = self.random.randrange(2, 4)
        senses = self.random.randrange(1, 5)
        is_individualist = self.random.random() * 100 <= self.individualist_percent
        while self.is_occupied(pos:=(
            self.random.randrange(self.width),
            self.random.randrange(self.height)
        )):
            pass

        ant = Ant(
            pos=pos,
            model=self,
            moore=False,
            sugar=sugar,
            metabolism=metabolism,
            senses=senses,
            individualist=is_individualist,
        )
        self.grid.place_agent(ant, pos)
        self.schedule.add(ant)

    def is_occupied(self, pos):
        this_cell = self.grid.get_cell_list_contents([pos])
        return len(this_cell) > 1

    def step(self):
        self.schedule.step()

        # collect data
        self.datacollector.collect(self)

        if self.recreate and self.schedule.time % 10 == 0:
            for _ in range(0, self.recreate):
                self._create_ant()

        if self.verbose:
            print({
                'time': self.schedule.time,
                '% dead ': self.schedule.percent_dead(),
                '% dead high senses': self.schedule.percent_dead(filter=self.PERCENT_DEAD_HIGH_SENSES),
                '% dead low senses': self.schedule.percent_dead(filter=self.PERCENT_DEAD_LOW_SENSES),
            })

    def run_model(self, step_count=200):

        if self.verbose:
            print(
                "Initial number Sugarscape Agent: ",
                self.schedule.get_breed_count(Ant),
            )

        for _ in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print(
                "Final number Sugarscape Agent: ",
                self.schedule.get_breed_count(Ant),
            )
