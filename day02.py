#!/usr/bin/env python3

import argparse

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=str)

    return ap.parse_args()

def part_1(commands):
    depth = 0
    horiz = 0
    for line in commands:
        line = line.split()
        cmd = line[0]
        num = int(line[1])

        if cmd == "forward":
            horiz += num
        elif cmd == "down":
            depth += num
        elif cmd == "up":
            depth -= num

    print(depth * horiz)

def part_2(commands):
    aim = 0
    depth = 0
    horiz = 0
    for line in commands:
        line = line.split()
        cmd = line[0]
        num = int(line[1])

        if cmd == "forward":
            horiz += num
            depth += aim * num
        elif cmd == "down":
            aim += num
        elif cmd == "up":
            aim -= num

    print(depth * horiz)


if __name__ == '__main__':
    commands = _parse_args().input.split('\n')
    part_1(commands)
    part_2(commands)
