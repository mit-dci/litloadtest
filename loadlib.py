import time
import random

import testlib

def square_pos(size, x, y):
    return size * (y % size) + (x % size)

# Makes a big grid of nodes, all connected to their neighbors.
def make_grid_env(size):
    print('Making grid env of size', size)
    env = testlib.TestEnv(size ** 2)
    for l in env.lits:
        l.rpc.SetFee(Fee=5, CoinType=testlib.REGTEST_COINTYPE)
        a = l.make_new_addr()
        res = env.bitcoind.rpc.sendtoaddress(a, 10)
        print('Funded', a, 'with', res)
    env.generate_block()
    for x in range(size):
        for y in range(size):
            pos = square_pos(size, x, y)
            litat = env.lits[pos]
            print(pos, ':', x, y, '->', str(litat.get_balance_info()))
            if x > 0:
                litl = env.lits[square_pos(size, x - 1, y)] # l = left
                litat.connect_to_peer(litl)
                litat.open_channel(litl, 100000000, 200000)
                env.generate_block()
            if y > 0:
                litu = env.lits[square_pos(size, x, y - 1)] # u = up
                litat.connect_to_peer(litu)
                litat.open_channel(litu, 100000000, 200000)
                env.generate_block()
    env.generate_block(count=5)
    return env

def random_node_pair(env):
    x = random.randint(0, len(env.lits) - 1)
    y = random.randint(0, len(env.lits) - 2)
    if y >= x:
        y += 1
    return env.lits[x], env.lits[y]
