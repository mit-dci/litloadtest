#!/usr/bin/env python3

import time
import multiprocessing
import random
import traceback
import shutil

import testlib
import loadlib

grid_edge_len = 3 # 9 nodes total

threads = 1
payments = 100

delay = 0.25
jitter = 0.05

def main(env):
    tasks = []
    for i in range(payments):
        src, dst = loadlib.random_node_pair(env)
        tasks.append({
            'from': src.rpc,
            'fromaddr': src.lnid,
            'fromaddrfull': src.lnid + '@127.0.0.1:' + str(src.p2p_port),
            'to': dst.rpc,
            'toaddr': dst.lnid,
            'toaddrfull': dst.lnid + '@127.0.0.1:' + str(dst.p2p_port),
        })

    print('Running payments...')
    p = multiprocessing.Pool(threads)
    res = p.map(run_multihop_payment, tasks)
    time.sleep(1)

def wait_delay():
    time.sleep(delay + random.uniform(jitter * -1, jitter))

def run_multihop_payment(task):
    print(task['fromaddr'], '->', task['toaddr'])
    srcrpc = task['from']
    conns = srcrpc.ListConnections()
    connected = False
    for p in conns['Connections']:
        if p['LitAdr'] == task['toaddr']:
            connected = True
            print('already connected, no need for new connection')
    if not connected:
        res = srcrpc.Connect(LNAddr=task['toaddrfull']) # might have duplicate connections
        print(str(res))
    time.sleep(0.1)
    res = srcrpc.PayMultihop(
        DestLNAdr=task['toaddr'],
        DestCoinType=testlib.REGTEST_COINTYPE,
        OriginCoinType=testlib.REGTEST_COINTYPE,
        Amt=120000) # has to be >105000
    print(str(res))

if __name__ == '__main__':
    shutil.rmtree(testlib.get_root_data_dir())
    env = None
    try:
        env = loadlib.make_grid_env(grid_edge_len)
        main(env)
    except:
        traceback.print_exc()
        if env is not None:
            env.shutdown()
