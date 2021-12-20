#!/usr/bin/env python3

import argparse
from collections import namedtuple
from typing import List


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=str)

    return ap.parse_args()


class BingoCell:
    def __init__(self, num):
        self.num = int(num)
        self.marked = False

    def __repr__(self):
        if self.num < 10:
            return f'0{self.num}'
        return f'{self.num}'


class Bingo:
    def __init__(self, input):
        lines = input.split('\n')
        self.numbers = [int(i) for i in lines[0].split(',')]
        self.curr_num_idx = 0

        self.boards = []

        board = []
        for line in lines[2:]:
            if len(line) == 0:
                self.boards.append(board)
                board = []
            else:
                board.append([BingoCell(num) for num in line.split()])
        self.boards.append(board)

        self.size = len(self.boards[0])

    def turn(self):
        num = self.numbers[self.curr_num_idx]
        self.curr_num_idx += 1

        for board in self.boards:
            for row in board:
                for cell in row:
                    if cell.num == num:
                        cell.marked = True

    def winners(self) -> List[bool]:
        winners = [False for _ in self.boards]

        for i, board in enumerate(self.boards):
            if any(all(cell.marked for cell in row) for row in board):
                winners[i] = True
                continue

            for col in range(self.size):
                if all(row[col].marked for row in board):
                    winners[i] = True

        return winners

    def sum_unmarked(self) -> List[int]:
        return [
            sum(cell.num for row in board for cell in row if not cell.marked)
            for board in self.boards
        ]

    def __repr__(self) -> str:
        res = ''
        for board in self.boards:
            for row in board:
                res += str(row) + '\n'
            res += '\n'
        return res


def part_1(args):
    bingo = Bingo(args)

    while not any(bingo.winners()):
        bingo.turn()

    sums = bingo.sum_unmarked()

    for pos, win in enumerate(bingo.winners()):
        if win:
            print(sums[pos] * bingo.numbers[bingo.curr_num_idx - 1])


def part_2(args):
    bingo = Bingo(args)

    while bingo.winners().count(False) != 1:
        bingo.turn()

    loser = bingo.winners().index(False)

    while not all(bingo.winners()):
        bingo.turn()

    last_num = bingo.numbers[bingo.curr_num_idx-1]
    print(bingo.sum_unmarked()[loser] * last_num)


if __name__ == '__main__':
    input = _parse_args().input
    part_1(input)
    part_2(input)
