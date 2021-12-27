#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Set, Tuple

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


class Grid:
    def __init__(self, input: str):
        self.grid = set()
        for line in input.split('\n'):
            try:
                self.grid.add(tuple(map(int, line.split(","))))
            except ValueError:
                break

        self.folds = []
        for line in input.split('\n'):
            try:
                dim, val = line.split("fold along ")[1].split('=')
                self.folds.append((dim, int(val)))
            except (ValueError, IndexError):
                pass

    def __repr__(self) -> str:
        x_max = max(x for x, _ in self.grid)
        y_max = max(y for _, y in self.grid)
        x_min = min(x for x, _ in self.grid)
        y_min = min(y for _, y in self.grid)
        return "\n".join(
                "".join(
                    '#' if (i, j) in self.grid else '.'
                    for i in range(x_min, x_max+1)
                )
                for j in range(y_min, y_max+1)
        )

    def fold(self):
        dim, val = self.folds.pop(0)
        match dim:
            case 'x':
                self.grid = set(
                        (2*val-x, y)
                        if x > val
                        else (x, y)
                        for x, y in self.grid
                )
            case 'y':
                self.grid = set(
                        (x, 2*val-y)
                        if y > val
                        else (x, y)
                        for x, y in self.grid
                )
            case _:
                raise ValueError("")


def part_1(input):
    grid = Grid(input)
    grid.fold()
    print(len(grid.grid))


def part_2(input):
    grid = Grid(input)
    while grid.folds:
        grid.fold()
    print(grid)


if __name__ == '__main__':
    input = _parse_args().input.read_text()

    part_1(input)
    part_2(input)
