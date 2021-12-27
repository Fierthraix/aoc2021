#!/usr/bin/env python3

import argparse
from functools import reduce
from operator import mul
from pathlib import Path
from typing import List, Tuple


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


def make_grid(text: str) -> List[List[int]]:
    return [[int(num) for num in line] for line in text.split('\n') if line]


def minima(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Get the local minima of a grid."""
    return [
            (i, j)
            for i in range(len(grid))
            for j in range(len(grid[0]))
            if (i == 0 or grid[i-1][j] > grid[i][j]) \
                and (i == len(grid)-1 or grid[i+1][j] > grid[i][j]) \
                and (j == 0 or grid[i][j-1] > grid[i][j]) \
                and (j == len(grid[0])-1 or grid[i][j+1] > grid[i][j])
            ]


def part_1(input):
    grid = make_grid(input)
    print(sum(grid[i][j] + 1 for i, j in minima(grid)))


def neighbours(grid: List[List[int]], point: Tuple[int, int]):
    """Get basin neighbours."""
    neighbours = []
    x, y = point
    x_max, y_max = len(grid)-1, len(grid[0])-1
    if x != 0 and grid[x-1][y] != 9:
        neighbours.append((x-1, y))
    if x != x_max and grid[x+1][y] != 9:
        neighbours.append((x+1, y))
    if y != 0 and grid[x][y-1] != 9:
        neighbours.append((x, y-1))
    if y != y_max and grid[x][y+1] != 9:
        neighbours.append((x, y+1))

    return neighbours


def basin(grid: List[List[int]], start: Tuple[int, int]) -> List[Tuple[int, int]]:
    nodes = set()
    new_nodes = set([start])

    while True:
        nodes |= new_nodes
        new_nodes = set(neighbour for node in new_nodes for neighbour in neighbours(grid, node))
        if new_nodes.issubset(nodes):
            break
    return nodes


def part_2(input):
    grid = make_grid(input)
    basin_sizes = sorted([len(basin(grid, minima)) for minima in minima(grid)], reverse=True)

    print(reduce(mul, (basin_sizes[i] for i in range(3)), 1))


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
