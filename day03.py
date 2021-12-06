#!/usr/bin/env python3

import argparse
from typing import *

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=str)

    return ap.parse_args()


def bit_sum(bit):
    if bit == '1':
        return 1
    if bit == '0':
        return -1


def sum_to_bit(num):
    if num < 0:
        return '0'
    return '1'


def bit_avg(num_list):
    avg = [0 for _ in range(len(num_list[0]))]

    for num in num_list:
        for i, bit in enumerate(num):
            avg[i] += bit_sum(bit)

    return ''.join(sum_to_bit(num) for num in avg)


def invert(num):
    invert = lambda num: '1' if num == '0' else '0'
    return ''.join(invert(digit) for digit in num)


def part_1(nums):
    gamma_bin = bit_avg(nums)
    epsilon_bin = invert(gamma_bin)
    gamma = int(gamma_bin, 2)
    epsilon = int(epsilon_bin, 2)
    print(gamma * epsilon)


def most_common_bit(pos: int, nums: List[str]) -> str:
    avg = 0
    for num in nums:
        avg += bit_sum(num[pos])
    return sum_to_bit(avg)


def filter_by_bit(bit: str, pos: int, num: str) -> bool:
    return num[pos] == bit


def part_2(nums):
    def pare_down_list(nums, bit_func):
        bits = len(nums[0])

        for pos in range(bits):
            bit_filter = lambda num: num[pos] == bit_func(pos, nums)
            nums = list(filter(bit_filter, nums))
            if len(nums) == 1:
                return nums[0]

    o2_func = most_common_bit
    co2_func = lambda pos, nums: invert(most_common_bit(pos, nums))

    oxygen_bin = pare_down_list(nums, o2_func)
    carbon_dioxide_bin = pare_down_list(nums, co2_func)

    oxygen = int(oxygen_bin, 2)
    carbon_dioxide = int(carbon_dioxide_bin, 2)

    print(oxygen * carbon_dioxide)


if __name__ == '__main__':
    input = _parse_args().input.split()
    part_1(input)
    part_2(input)
