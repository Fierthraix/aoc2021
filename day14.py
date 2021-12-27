#!/usr/bin/env python3

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


class Polymer:
    def __init__(self, input: str):
        self.template = input.split('\n')[0]
        # Group by pairs.
        self.pairs = Counter([f"{l}{r}" for l, r, in zip(self.template, self.template[1:])])
        self.rules = {
                pair: (pair[0] + sub, sub + pair[1])
                for pair, sub in
                (rule.split(' -> ') for rule in input.split('\n')[2:-1])
        }

    def step(self):
        new_pairs = {key: 0 for key in self.rules.keys()}
        for pair, count in self.pairs.items():
            new_pairs[self.rules[pair][0]] += count
            new_pairs[self.rules[pair][1]] += count
        self.pairs = new_pairs

    def letter_count(self) -> Counter[object, int]:
        counter = defaultdict(lambda: 0)

        for (left, right), count in self.pairs.items():
            counter[left] += count
            counter[right] += count

        for letter in counter:
            counter[letter] //= 2

        counter[self.template[-1]] += 1
        return Counter(counter)


def part_1(input):
    poly = Polymer(input)
    for _ in range(10):
        poly.step()

    stats = poly.letter_count()
    print(stats.most_common(1)[0][1] - stats.most_common()[-1][1])


def part_2(input):
    poly = Polymer(input)
    for _ in range(40):
        poly.step()

    stats = poly.letter_count()
    print(stats.most_common(1)[0][1] - stats.most_common()[-1][1])


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
