#!/usr/bin/env python3

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


def irange(num1, num2) -> range:
    if num1 < num2:
        start, stop = num1, num2
    else:
        start, stop = num2, num1
    return range(start, stop+1)


class Point():
    def __init__(self, coords: str):
        coords = coords.split(',')
        self.x = int(coords[0])
        self.y = int(coords[1])

    def __repr__(self) -> str:
        return f'({self.x},{self.y})'


class Line():
    def __init__(self, line: str):
        self.a, self.b = map(Point, line.split(' -> '))

    def is_ortho(self) -> bool:
        return self.a.x == self.b.x or self.a.y == self.b.y

    def __repr__(self) -> str:
        return f"<< {self.a.x},{self.a.y} -> {self.b.x},{self.b.y} >>"


def get_ortho_points(lines: List[Line]) -> Dict[Tuple[int, int], int]:
    points = defaultdict(lambda: 0)

    for line in lines:
        if line.a.x == line.b.x:
            for y in irange(line.a.y, line.b.y):
                points[(line.a.x, y)] += 1
        elif line.a.y == line.b.y:
            for x in irange(line.a.x, line.b.x):
                points[(x, line.a.y)] += 1

    return points


def count_overlaps(points: Dict[Tuple[int, int], int]) -> int:
    return sum(1 for (_, overlaps) in points.items() if overlaps > 1)


def part_1(args):
    lines = [Line(line) for line in args.split('\n') if line and Line(line).is_ortho()]
    print(count_overlaps(get_ortho_points(lines)))


def part_2(args):
    lines = [Line(line) for line in args.split('\n') if line]

    ortho = [line for line in lines if line.is_ortho()]
    diags = [line for line in lines if not line.is_ortho()]

    points = get_ortho_points(ortho)

    for line in diags:
        if line.a.x < line.b.x:
            x0 = line.a.x
            y0 = line.a.y
            up = y0 < line.b.y
        else:
            x0 = line.b.x
            y0 = line.b.y
            up = y0 < line.a.y

        for d in range(abs(line.a.x - line.b.x) + 1):
            if up:
                points[(x0 + d, y0 + d)] += 1
            else:
                points[(x0 + d, y0 - d)] += 1

    print(count_overlaps(points))


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
