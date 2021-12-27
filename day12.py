#!/usr/bin/env python3

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)

    return ap.parse_args()


START = 'start'
END = 'end'


def is_small(cave: str) -> bool:
    return cave.lower() == cave


def is_big(cave: str) -> bool:
    return not is_small(cave)


def exists_repeating_subsequence(seqs: List[object]) -> bool:
    max_len = len(seqs) // 2

    for start in range(len(seqs) - 1):
        for seq_len in range(4, (len(seqs) - start + 1) // 2):
            curr_seq = seqs[start:start + seq_len]
            for trial_start in range(start + seq_len, len(seqs) - seq_len + 1):
                trial = seqs[trial_start:trial_start + seq_len]
                if curr_seq == trial:
                    return True
    return False


class Graph:
    def __init__(self, edges: str):
        self.adj = defaultdict(set)
        self.exits = None
        for edge in edges.split('\n'):
            if not edge:
                continue
            a, b = edge.split('-')
            self.adj[a].add(b)
            self.adj[b].add(a)

    @classmethod
    def _find_exits(cls, adj: Dict[str, List[str]], path: List[str]) -> List[List[str]]:
        results = []
        for next_node in adj[path[-1]]:
            next_path = path.copy() + [next_node]
            if next_node == END:
                results.append(next_path)
            elif next_node == START or is_small(next_node) and next_node in path:
                continue
            else:
                results += cls._find_exits(adj, next_path)
        return results

    def find_exits(self) -> Set[Tuple[str]]:
        return set(
                tuple(exit)
                for exit in self._find_exits(self.adj, [START])
                if not exists_repeating_subsequence(exit)
        )

    @classmethod
    def _find_exits_revisted(
            cls,
            adj: Dict[str, List[str]],
            path: List[str],
            double: Optional[str]
    ) -> List[List[str]]:
        results = []
        for next_node in adj[path[-1]]:
            next_path = path.copy() + [next_node]
            match next_node:
                case 'start':
                    continue
                case 'end':
                    results.append(next_path)
                    continue

            if is_small(next_node) and next_node in path:
                if double is None:  # We now have a doubled character.
                    results += cls._find_exits_revisted(adj, next_path, next_node)
            else:  # Big rooms can be visited a lot.
                results += cls._find_exits_revisted(adj, next_path, double)

        return results

    def find_exits_revisted(self) -> Set[Tuple[str]]:
        return set(
                tuple(exit)
                for exit in self._find_exits_revisted(self.adj, [START], None)
                if not exists_repeating_subsequence(exit)
        )


def part_1(input):
    cave = Graph(input)
    print(len(cave.find_exits()))


def part_2(input):
    cave = Graph(input)
    print(len(cave.find_exits_revisted()))


if __name__ == '__main__':
    input = _parse_args().input.read_text()
    part_1(input)
    part_2(input)
