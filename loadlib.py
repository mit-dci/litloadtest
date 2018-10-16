import randint

import testlib

def square_pos(size, x, y):
    return size * (y % size) + (x % size)

# Makes a big grid of nodes, all connected to their neighbors.
def make_grid_env(size):
    print('Making grid env of size', size)
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
                    litl = env.lits[square_pos(size, x - 1, y)] # l = left
                    litat.connect_to_peer(litl)
                if y > 0:
                    litu = env.lits[square_pos(size, x, y - 1)] # u = up
                    litat.connect_to_peer(litu)
        return env
    except:
        if env is not None:
            env.shutdown()
        return None

def exec_multihop_spend(lit1, lit2):
    pass # TODO

def random_node_pair(env):
    x = random.randint(len(env.lits))
    y = random.randint(len(env.lits) - 1)
    if y >= x:
        y += 1
    return env.lits[x], env.lits[y]
