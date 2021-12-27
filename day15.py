#!/usr/bin/env python3

import argparse
from heapq import heappop, heappush
from itertools import product
from pathlib import Path
from typing import List, Tuple


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()

class RiskAssesser:
    def __init__(self, grid: str):
        self.grid = [[int(num) for num in row] for row in grid.split('\n') if row]

    def find_best_path(self, scale_factor: int = 1) -> List[Tuple[int, int]]:
        x_max, y_max = len(self.grid), len(self.grid[0])
        heap = [(0, 0, 0)]
        seen = {(0, 0)}
        while heap:
            risk, i, j = heappop(heap)
            if i == scale_factor * x_max - 1 and j == scale_factor * y_max - 1:
                return risk

            for x, y in (i-1, j), (i+1, j), (i, j-1), (i, j+1):
                if 0 <= x < scale_factor * x_max \
                    and 0 <= y < scale_factor * y_max \
                    and (x, y) not in seen:
                        ii, im = divmod(x, x_max)
                        ji, jm = divmod(y, y_max)

                        seen.add((x, y))
                        heappush(heap, (risk + (self.grid[im][jm] + ii + ji - 1) % 9 + 1, x, y))

def part_1(input):
    risker = RiskAssesser(input)
    print(risker.find_best_path())


def part_2(input):
    risker = RiskAssesser(input)
    print(risker.find_best_path(scale_factor=5))


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
