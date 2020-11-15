from typing import Optional
from collections import defaultdict

from mesa.time import RandomActivation

from .agents import Ant

LOW_VISION_THRESHOLD = 3


class RandomActivationByBreed(RandomActivation):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step() method.
    """

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_breed = defaultdict(dict)
        self.num_dead = 0
        self.num_low_vision_dead = 0
        self.num_high_vision_dead = 0

    def add(self, agent):
        """
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        """

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.agents_by_breed[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.
        """

        self.num_dead += 1
        if agent.vision < LOW_VISION_THRESHOLD:
            self.num_low_vision_dead += 1
        else:
            self.num_high_vision_dead += 1

        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_breed[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        """
        Executes the step of each agent breed, one at a time, in random order.

        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        """
        if by_breed:
            for agent_class in self.agents_by_breed:
                self.step_breed(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_breed(self, breed):
        """
        Shuffle order and run all agents of a given breed.

        Args:
            breed: Class object of the breed to run.
        """
        agent_keys = list(self.agents_by_breed[breed].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_breed[breed][agent_key].step()

    def get_breed_count(self, breed_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        return len(self.agents_by_breed[breed_class].values())

    def percent_dead(self, filter: Optional[str]=None) -> float:
        if self.num_dead == 0:
            return 0

        if filter:
            value = 0
            if filter == self.model.PERCENT_DEAD_LOW_VISION:
                value = self.num_low_vision_dead
            elif filter == self.model.PERCENT_DEAD_HIGH_VISION:
                value = self.num_high_vision_dead
            return value/self.num_dead
        else:
            self.num_dead/(self.num_dead + self.get_breed_count(Ant))
