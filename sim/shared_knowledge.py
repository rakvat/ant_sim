import sys
import math
import random
from mesa.space import MultiGrid

from .agents import Sugar


POS = tuple[int, int]


class SharedKnowledge:
    distance_map: dict[POS, float] = {}
    recent_sugar_map: dict[POS, int] = {}
    current_max = 0

    def __init__(self, grid: MultiGrid):
        self.grid = grid
        self.width = grid.width
        self.height = grid.height

        for i in range(0, self.width):
            for j in range(0, self.height):
                self.distance_map[(i, j)] = math.sqrt(i**2+j**2)
                self.recent_sugar_map[(i,j)] = self._sugar_at((i, j))

    def update(self) -> None:
        for _, x, y in self.grid.coord_iter():
            self.recent_sugar_map[(x, y)] = round(self.recent_sugar_map[(x,y)] * 0.5 + 0.5 * self._sugar_at((x, y)))
        print(self.recent_sugar_map)

    def recent_max(self) -> int:
        if not self.recent_sugar_map:
            return 0
        return max(self.recent_sugar_map.values())

    def distance(self, pos_a: POS, pos_b: POS) -> float:
        return self.distance_map[(abs(pos_a[0]-pos_b[0]), abs(pos_a[1]-pos_b[1]))]

    def _sugar_at(self, pos: POS) -> int:
        for agent in self.grid[pos]:
            if type(agent) is Sugar:
                return agent.amount
        return 0

    def _closest(self, pos:POS, candidates: list[POS]) -> POS:
        min_dist = sys.maxsize
        random.shuffle(candidates)
        min_dist_pos = candidates[0]
        for max_pos in candidates:
            dist = self.distance(pos, max_pos)
            if dist < min_dist:
                min_dist_pos = max_pos
                min_dist = dist
        return min_dist_pos

    def closest_max(self, pos: POS) -> POS:
        recent_max = self.recent_max()
        pos_with_max: list[POS] = [
            pos for pos, value in self.recent_sugar_map.items() if value >= recent_max
        ]
        if not pos_with_max:
            return pos
        return self._closest(pos, pos_with_max)

    def in_direction_to_closest_max(self, current_pos: POS, candidates: list[POS]) -> POS:
        closest = self.closest_max(current_pos)

        min_pos = current_pos
        min_dist = sys.maxsize
        random.shuffle(candidates)
        for u_pos in candidates:
            dist = self.distance(u_pos, closest)
            if dist < min_dist:
                min_dist = dist
                min_pos = u_pos

        return min_pos
