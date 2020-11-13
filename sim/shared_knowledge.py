import sys
import random
from typing import Dict, Tuple, List


POS = Tuple[int, int]


class SharedKnowledge:
    distance_map: Dict[POS, float] = {}
    max_sugar_map: Dict[POS, int] = {}
    current_max = 0

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        print("width", width)
        print("height", height)

        for i in range(0, width):
            for j in range(0, height):
                self.distance_map[(i, j)] = (i**2+j**2)/2

    def publish_value(self, pos: POS, value: int) -> None:
        self.current_max = max(value, self.current_max)
        self.max_sugar_map[pos] = max(value, self.max_sugar_map.get(pos, 0))

    def distance(self, pos_a: POS, pos_b: POS) -> float:
        return self.distance_map[(abs(pos_a[0]-pos_b[0]), abs(pos_a[1]-pos_b[1]))]

    def closest_max(self, pos: POS) -> POS:
        pos_with_max: List[POS] = [
            pos for pos, value in self.max_sugar_map.items() if value >= self.current_max
        ]
        if not pos_with_max:
            return pos
        min_dist = sys.maxsize
        random.shuffle(pos_with_max)
        min_dist_pos = pos_with_max[0]
        for max_pos in pos_with_max:
            dist = self.distance(pos, max_pos)
            if dist < min_dist:
                min_dist_pos = max_pos
                min_dist = dist

        return min_dist_pos

    def in_direction_to_closest_max(self, pos: POS, unoccupied_pos: List[POS]) -> POS:
        print("current", pos)
        closest = self.closest_max(pos)

        min_pos = pos
        min_dist = sys.maxsize
        random.shuffle(unoccupied_pos)
        for u_pos in unoccupied_pos:
            dist = self.distance(u_pos, closest)
            if dist < min_dist:
                min_dist = dist
                min_pos = u_pos

        print("closest", closest)
        print("min pos", min_pos)
        return min_pos
