#!/usr/bin/env python3

import argparse
from collections import defaultdict
from pathlib import Path


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


class Fish:
    """A Lanternfish."""
    def __init__(self, timer: int = 8):
        self.timer = timer

    def reproduce(self) -> bool:
        if self.timer == 0:
            self.timer = 6
            return True
        self.timer -= 1
        return False


class School:
    def __init__(self, state: str):
        self.fishes = [Fish(int(num)) for num in state.split(',')]

    def run_day(self):
        new_fishes = [Fish() for fish in self.fishes if fish.reproduce()]
        self.fishes += new_fishes

    @property
    def num_fishes(self) -> int:
        return len(self.fishes)


def part_1(input):
    num_days = 80
    fishes = School(input)

    for _ in range(num_days):
        fishes.run_day()

    print(fishes.num_fishes)


class BigSchool:
    repro_cycle = 8

    def __init__(self, state: str):
        self.fishes = defaultdict(lambda: 0)

        for fish in state.split(','):
            self.fishes[int(fish)] += 1

    def run_day(self):
        new_school = defaultdict(lambda: 0)

        # new fish from reproduction
        new_school[8] += self.fishes[0]

        # reset timer for 0 fish
        new_school[6] += self.fishes[0]

        # move the others
        for day in range(max(self.fishes.keys())):
            new_school[day] += self.fishes[day + 1]

        self.fishes = new_school

    @property
    def num_fishes(self) -> int:
        return sum(self.fishes.values())


def part_2(input):
    num_days = 256
    fishes = BigSchool(input)

    for _ in range(num_days):
        fishes.run_day()

    print(fishes.num_fishes)


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
