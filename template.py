#!/usr/bin/env python3

import argparse

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', nargs=1, type=str)

    return ap.parse_args()

def run(args):
    pass


if __name__ == '__main__':
    run(_parse_args())
