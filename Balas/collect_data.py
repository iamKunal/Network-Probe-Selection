#!/usr/bin/env python

from pwn import *

import math

context.log_level='error'

n = 4
step = 1
max_n = 40 + 1

data=[]

for i in xrange(n, max_n, step):
    r = process('./bal.py')

    r.sendline('%d %d %d' %(i, i, math.ceil(i**0.5)+1))
    cur=[i]
    o = r.recvall().split('\n')
    for line in o:
        if('Time' in line or 'Iterations' in line):
            cur.append(float(line.split()[-1]))
    data.append(cur)
    for d in data:
        print d
    r.kill()

with open('data/p_vs_iter_k3.csv', 'w') as f:
    f.write('Number of Probes\tIterations\tSolution Time\tMatrix Time\n')
    for d in data:
        i,m,it,t=d
        f.write('%d\t%d\t%f\t%f\n' %(i,it,t,m))

