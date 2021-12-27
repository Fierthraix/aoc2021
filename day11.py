#!/usr/bin/env python3

import argparse
from itertools import product
from pathlib import Path
from typing import Iterator, Tuple

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


class Octopode:
    def __init__(self, grid: str):
        self.octopi = [[int(col) for col in row] for row in grid.split('\n') if row]

    def increment(self):
        for x in range(len(self.octopi)):
            for y in range(len(self.octopi[0])):
                self.octopi[x][y] += 1

    def get_neighbours(self, x0, y0) -> Iterator[Tuple[int, int]]:
        adjacent = lambda p: (p-1, p, p+1)
        return (
                (x, y)
                for x, y in product(adjacent(x0), adjacent(y0))
                if (x, y) != (x0, y0)
                if x >= 0 and y >= 0
                if x < len(self.octopi)
                if y < len(self.octopi[0])
        )

    @property
    def num_octopi(self):
        return len(self.octopi) * len(self.octopi[0])

    def flash(self, x0, y0):
        if self.octopi[x0][y0] < 10:
            return 0

        for x, y in self.get_neighbours(x0, y0):
            if self.octopi[x][y] > 0:
                self.octopi[x][y] += 1
        self.octopi[x0][y0] = 0
        return 1


    def step(self):
        flashes = 0
        self.increment()
        while True:
            new_flashes = sum(
                    self.flash(x, y)
                    for x, row in enumerate(self.octopi)
                    for y, octopus in enumerate(row)
            )
            if new_flashes:
                flashes += new_flashes
            else:  # No new flashes, step complete.
                break

        return flashes

    def __repr__(self):
        return "\n".join(
                "".join(
                    str(octopus)
                    if octopus else "༳"
                    for octopus in row
                )
                for row in self.octopi
        )



def part_1(input):
    octopode = Octopode(input)
    flashes = sum(octopode.step() for _ in range(100))
    print(flashes)


def part_2(input):
    octopode = Octopode(input)
    step = 1
    while octopode.step() != octopode.num_octopi:  # Wait until all octopi flash.
        step += 1
    print(step)


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
