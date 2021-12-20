#!/usr/bin/env python3

import argparse
from pathlib import Path

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


def part_1(input):
    pass


def part_2(input):
    pass


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
