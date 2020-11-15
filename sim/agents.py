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
    def __init__(self, id, pos, model, moore=False, sugar=0, metabolism=0, vision=0):
        super().__init__(pos, model)
        self.id = id
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision

    def get_sugar(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent

    def move_with_shared_knowledge(self):
        neighbors = self.unoccupied_neighbors()
        candidates = []
        if neighbors:
            candidates = self.max_sugar_candidates(neighbors)

        new_pos = self.model.shared_knowledge.in_direction_to_closest_max(
            current_pos=self.pos,
            candidates=candidates,
        )
        sugar_at_new_pos = self.get_sugar(new_pos).amount
        self.model.shared_knowledge.publish_value(new_pos, sugar_at_new_pos)
        self.model.grid.move_agent(self, new_pos)

    def unoccupied_neighbors(self):
        return [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, False, radius=self.vision
            )
            if not self.model.is_occupied(i)
        ]

    def max_sugar_candidates(self, possible_pos):
        max_sugar = max([self.get_sugar(pos).amount for pos in possible_pos])
        return [pos for pos in possible_pos if self.get_sugar(pos).amount == max_sugar]


    def move(self):
        neighbors = self.unoccupied_neighbors()
        neighbors.append(self.pos)
        candidates = self.max_sugar_candidates(neighbors)
        # Narrow down to the nearest ones
        min_dist = min([get_distance(self.pos, pos) for pos in candidates])
        final_candidates = [
            pos for pos in candidates if get_distance(self.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def eat(self):
        sugar_patch = self.get_sugar(self.pos)
        self.sugar = self.sugar - self.metabolism + sugar_patch.amount
        sugar_patch.amount = 0

    def step(self):
        if self.model.shared_knowledge:
            self.move_with_shared_knowledge()
        else:
            self.move()
        self.eat()
        if self.sugar <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)


class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = min([self.max_sugar, self.amount + 1])
