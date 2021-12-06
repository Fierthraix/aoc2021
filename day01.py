#!/usr/bin/env python3

import argparse

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=str)

    return ap.parse_args()

def increase(list1, list2):
    total = 0
    for num1, num2 in zip(list1, list2):
        if num2 > num1:
            total += 1

    return total


def part_1(nums):
    print(increase(nums, nums[1:]))


def part_2(nums):
    windows = [i + j + k for i, j, k in zip(nums, nums[1:], nums[2:])]
    print(increase(windows, windows[1:]))


if __name__ == '__main__':
    nums = [int(i) for i in _parse_args().input]
    part_1(nums)
    part_2(nums)
