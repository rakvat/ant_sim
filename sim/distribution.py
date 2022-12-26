import sys
import math
import random
from typing import Dict, Tuple, List


POS = Tuple[int, int]


class Distribution:

    def __init__(self):
        self.amount = 0

    def add(self, amount: int) -> None:
        assert amount >= 0
        self.amount += amount

    def require(self, amount:int) -> int:
        available = amount if self.amount >= amount else self.amount
        self.amount -= available
        assert self.amount >= 0
        return available

