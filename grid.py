#!/usr/bin/env python3

import testlib

grid_edge_len = 5

def square_pos(size, x, y):
    return size * (y % size) + (x % size)

# Makes a big grid of nodes, all connected to their neighbors.
def make_grid(size):
    print('Making grid of size', size)
    env = None
    try:
        env = testlib.TestEnv(size ** 2)
        for l in env.lits:
            a = l.make_new_addr(a, 1)
            env.bitcoind.rpc.sendtoaddress()
        for x in range(size):
            for y in range(size):
                litat = env.lits[square_pos(size, x, y)]
                if x > 0:
                    litl = env.lits[square_pos(size, x - 1, y)]
                    litat.connect_to_peer(litl)
                if y > 0:
                    litd = env.lits[square_pos(size, x, y - 1)]
                    litat.connect_to_peer(litd)
    except:
        if env is not None:
            env.shutdown()

def main():
    net = make_grid(3) # 9 nodes total
    # TODO

if __name__ == '__main__':
    main()
