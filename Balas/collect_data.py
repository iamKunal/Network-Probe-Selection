#!/usr/bin/env python

from pwn import *

import math

import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


context.log_level='error'

p = 25
step = 1
max_p = 35 + 1

for k in xrange(27,36):
    n=10
    data=[]

    for i in xrange(p, max_p, step):
        r = process('./bal.py')

        r.sendline('%d %d %d' %(k,i, 7))
        cur=[i]
        signal.alarm(5)    
        try:
            o = r.recvall().split('\n')
        except TimeoutException:
            continue # continue the for loop if function A takes more than 5 second
        else:
            # Reset the alarm
            signal.alarm(0)
        for line in o:
            if('Time' in line or 'Iterations' in line):
                cur.append(float(line.split()[-1]))
        data.append(cur)
        for d in data:
            print d
        r.kill()

    with open('data/p_vs_iter_p%d.csv' %(k), 'w') as f:
        f.write('Number of Probes\tIterations\tSolution Time\tMatrix Time\n')
        for d in data:
            i,m,it,t=d
            f.write('%d\t%d\t%f\t%f\n' %(i,it,t,m))

