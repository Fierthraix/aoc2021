#!/usr/bin/env python3

import argparse

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=str)

    return ap.parse_args()


def part_1(args):
    pass


def part_2(args):
    pass


if __name__ == '__main__':
    input = _parse_args().input.split()
    part_1(input)
    part_2(input)
