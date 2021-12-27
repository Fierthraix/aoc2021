#!/usr/bin/env python3

import argparse
from enum import Enum
from pathlib import Path
from typing import List, Optional

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


class DelimChar(Enum):
    CRL_L = '('
    SQR_L = '['
    SWG_L = '{'
    TRI_L = '<'
    CRL_R = ')'
    SQR_R = ']'
    SWG_R = '}'
    TRI_R = '>'

    def is_left(self):
        """Is it a lefthand delimiter?"""
        return self in (DelimChar.CRL_L, DelimChar.SQR_L, DelimChar.SWG_L, DelimChar.TRI_L)

    def is_right(self):
        """Is it a righthand delimiter?"""
        return not self.is_left()

    def matches(self, other) -> bool:
        """Do these characters complete each other?"""
        return {self.value, other.value} in ({'(', ')'}, {'[', ']'}, {'{', '}'}, {'<', '>'})

    def opposite(self) -> 'DelimChar':
        """Get the opposing character."""
        match self:
            case DelimChar.CRL_L:
                return DelimChar.CRL_R
            case DelimChar.SQR_L:
                return DelimChar.SQR_R
            case DelimChar.SWG_L:
                return DelimChar.SWG_R
            case DelimChar.TRI_L:
                return DelimChar.TRI_R

    @property
    def illegal_points(self):
        match self:
            case DelimChar.CRL_R:
                return 3
            case DelimChar.SQR_R:
                return 57
            case DelimChar.SWG_R:
                return 1197
            case DelimChar.TRI_R:
                return 25137
            case _:
                return 0

    @property
    def close_points(self):
        match self:
            case DelimChar.CRL_R:
                return 1
            case DelimChar.SQR_R:
                return 2
            case DelimChar.SWG_R:
                return 3
            case DelimChar.TRI_R:
                return 4
            case _:
                return 0


class Stack:
    def __init__(self, line: str):
        self.stack = [DelimChar(char) for char in line]

    def first_illegal(self) -> Optional[DelimChar]:
        stack = []
        for char in self.stack:
            if char.is_left():
                stack.append(char)
            else:
                if char.matches(stack[-1]):
                    stack.pop()
                else:
                    return char
        return None

    def is_legal(self) -> bool:
        return self.first_illegal() is None

    def complete_line(self) -> List[DelimChar]:
        stack = []
        for char in self.stack:
            if char.is_left():
                stack.append(char)
            else:
                if char.matches(stack[-1]):
                    stack.pop()

        return [char.opposite() for char in reversed(stack)]

    def complete_value(self) -> int:
        score = 0
        for char in self.complete_line():
            score *= 5
            score += char.close_points
        return score


def part_1(input):
    logs = [Stack(line) for line in input.split('\n')]
    illegals = filter(None, (line.first_illegal() for line in logs))
    score = sum(bad_val.illegal_points for bad_val in illegals)
    print(score)


def part_2(input):
    logs = [
            stack for stack in
            (Stack(line) for line in input.split('\n'))
            if stack.is_legal()
    ]

    scores = sorted([line.complete_value() for line in logs])
    print(scores[len(scores) // 2])


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
