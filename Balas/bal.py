#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from builtins import print

import numpy as np

solutions = []

a = np.matrix('1 0 1 0 0;1 0 0 1 1;1 1 0 0 1;0 0 0 1 1;0 1 1 0 0;0 0 1 1 0')
a = np.matrix('1 1 0 0 0;0 1 1 0 0;0 0 1 1 0;0 0 0 1 1;1 0 0 0 1')
# print(a)
# print(dir(a))
np.save('F.npy', a)

F = np.load('F.npy')
print(F)
C = F.sum(1)
p = C.size
# print(F.dtype)
n = F.size // p

k = [2] * n
k = np.array(k)

print("n=%d, p=%d" % (n, p))


def z(x):
    if type(x) == type(list):
        return C.T.dot(np.array(x))
    else:
        return C.T.dot(x)


def feasible(x):
    tru = F.T.dot(x) >= k
    tru = tru.tolist()
    satisfied = True
    for v in tru:
        satisfied = satisfied and v
    return satisfied


# print(feasible([1, 1, 1, 1, 1, 0]))


def main_checker(x):
    # if z(x) > z(parent):
    #     return False
    future_sol = x[:depth + 1]
    future_sol = future_sol + [1] * (p - depth - 1)
    # print(future_sol)
    return feasible(future_sol) and not feasible(x)


stack = [[[0] * p, -1]]

parent = []
wasInStack = [[0] * p]
iterations = 0
depth = -1
while stack:

    # break

    parent, depth = stack.pop()
    stack_size = len(stack)
    depth += 1
    left_sol = parent[:]
    left_sol[depth] = 0
    print("depth = ", depth)
    try:
        left_sol[depth + 1] = 1
        print("l : ", left_sol)
        if main_checker(left_sol):
            stack.append([left_sol, depth])
        elif feasible(left_sol):
            solutions.append(left_sol)

            # depth -= 1

    except IndexError:
        pass
    right_sol = parent[:]
    right_sol[depth] = 1

    print("r : ", right_sol)
    if main_checker(right_sol):
        stack.append([right_sol, depth])
    elif feasible(right_sol):
        solutions.append(right_sol)
        # depth -= 1
    print("stack : ", stack)

    # if stack_size == len(stack):
    #     depth -= 1

    print("sol : ", solutions)
    iterations += 1
    print("\ni :", iterations)
    if iterations > 32:
        break
# print(x.dtype)
# print(x.astype(int))
# print(C)
# print(Z(x.T))
