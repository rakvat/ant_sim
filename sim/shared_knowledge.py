import sys
import math
import random
from typing import Dict, Tuple, List


POS = Tuple[int, int]


class SharedKnowledge:
    distance_map: Dict[POS, float] = {}
    max_sugar_map: Dict[POS, int] = {}
    recent_sugar_map: Dict[POS, int] = {}
    current_max = 0

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        for i in range(0, width):
            for j in range(0, height):
                self.distance_map[(i, j)] = math.sqrt(i**2+j**2)

    def publish_value(self, pos: POS, value: int) -> None:
        self.current_max = max(value, self.current_max)
        self.max_sugar_map[pos] = max(value, self.max_sugar_map.get(pos, 0))
        self.recent_sugar_map[pos] = round(self.recent_sugar_map.get(pos, 0) * 0.5 + 0.5 * value)

    def recent_max(self) -> int:
        if not self.recent_sugar_map:
            return 0
        return max(self.recent_sugar_map.values())

    def distance(self, pos_a: POS, pos_b: POS) -> float:
        return self.distance_map[(abs(pos_a[0]-pos_b[0]), abs(pos_a[1]-pos_b[1]))]

    def _closest(self, pos:POS, candidates: List[POS]) -> POS:
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
        pos_with_max: List[POS] = [
            # pos for pos, value in self.max_sugar_map.items() if value >= self.current_max
            pos for pos, value in self.recent_sugar_map.items() if value >= recent_max
        ]
        if not pos_with_max:
            return pos
        return self._closest(pos, pos_with_max)

    def in_direction_to_closest(self, current_pos: POS, candidates: List[POS]) -> POS:
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
