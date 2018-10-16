#!/usr/bin/env python3

import multiprocessing

import loadlib

grid_edge_len = 3 # 9 nodes total

def main(env):
    # TODO Start some multiprocessing processes that go and call on random nodes.

if __name__ == '__main__':
    env = None
    try:
        env = make_grid(grid_edge_len)
        main(env)
    except:
        if env is not None:
            env.shutdown()
