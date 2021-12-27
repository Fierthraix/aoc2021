#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Tuple
from math import factorial


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


class Crabs:
    def __init__(self, crabs: str):
        self.crabs = [int(crab) for crab in crabs.split(',')]

    def cost(self, x: int) -> int:
        return sum(abs(crab - x) for crab in self.crabs)

    def min_cost(self) -> int:
        high = max(self.crabs)
        low = min(self.crabs)

        while True:
            pivot = (high + low) // 2
            left, curr, right = map(self.cost, (pivot - 1, pivot, pivot + 1))
            if left > curr < right:
                return curr
            elif left > curr > right:
                low = pivot
            elif left < curr < right:
                high = pivot


def part_1(input):
    crabs = Crabs(input)
    print(crabs.min_cost())


def triangle_num(n):
    """Determine \sum_(i=1)^n i (e.g., 1 + 2 + 3 + ... + n)"""
    return int(factorial(n + 1) // 2 / factorial(n - 1)) if n else 0


class CrabFuel(Crabs):
    def cost(self, x: int) -> int:
        return sum(triangle_num(abs(crab - x)) for crab in self.crabs)


def part_2(input):
    crabs = CrabFuel(input)
    print(crabs.min_cost())


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    #input = "16,1,2,0,4,2,7,1,2,14"
    part_1(input)
    part_2(input)
