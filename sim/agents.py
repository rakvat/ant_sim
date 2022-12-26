import math

from mesa import Agent


def get_distance(pos_1, pos_2):
    """ Get the distance between two point

    Args:
        pos_1, pos_2: Coordinate tuples for both points.

    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)


class Ant(Agent):
    counter: int = 0
    SUGER_UPPER_LIMIT = 100
    SUGAR_LOWER_LIMIT = 50

    def __init__(self, pos, model, moore=False, sugar=0, metabolism=0, senses=0, individualist=False):
        super().__init__(pos, model)
        self.id = Ant.counter
        Ant.counter += 1
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.senses = senses
        self.individualist = individualist

    def get_sugar(self, pos):
        for agent in self.model.grid[pos]:
            if type(agent) is Sugar:
                return agent

    def move(self):
        neighbors = self.unoccupied_neighbors()
        candidates = self.max_sugar_candidates(neighbors or [self.pos])
        # Narrow down to the nearest ones
        min_dist = min([get_distance(self.pos, pos) for pos in candidates])
        final_candidates = [
            pos for pos in candidates if get_distance(self.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def move_with_internet(self):
        neighbors = self.unoccupied_neighbors()
        candidates = self.max_sugar_candidates(neighbors or [self.pos])

        new_pos = self.model.internet.in_direction_to_closest_max(
            current_pos=self.pos,
            candidates=candidates,
        )
        sugar_at_new_pos = self.get_sugar(new_pos).amount
        self.model.grid.move_agent(self, new_pos)

    def unoccupied_neighbors(self):
        return [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, False, radius=self.senses
            )
            if not self.model.is_occupied(i)
        ]

    def max_sugar_candidates(self, possible_pos):
        max_value = max([self.get_sugar(pos).amount for pos in possible_pos])
        return [pos for pos in possible_pos if self.get_sugar(pos).amount == max_value]

    def collect(self) -> int:
        sugar_patch = self.get_sugar(self.pos)
        assert sugar_patch
        collected = sugar_patch.amount
        sugar_patch.amount = 0
        return collected

    def eat(self, amount: int) -> None:
        self.sugar = self.sugar - self.metabolism + amount

    def step(self):
        if self.model.internet:
            self.move_with_internet()
        else:
            self.move()
        collected = self.collect()
        if self.model.solidarity and not self.individualist:
            needed = self.metabolism
            to_distribute = max(0, collected - needed) if self.sugar > 3 * self.metabolism else 0
            to_eat = collected - to_distribute
            if to_eat < needed:
                to_eat += self.model.distribution.require(needed-to_eat)
            self.model.distribution.add(to_distribute)
            self.eat(to_eat)
        else:
            self.eat(collected)
        if self.sugar <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.id = pos
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = min([self.max_sugar, self.amount + 1])
