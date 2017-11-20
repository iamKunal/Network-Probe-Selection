#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from builtins import print
import math
import numpy as np
import time
import generate_test

solutions = []
a = input("Enter n, p, k : ").split()
a = map(int, a)
n, p, k = a

# a = np.matrix('1 0 1 0 0;1 0 0 1 1;1 1 0 0 1;0 0 0 1 1;0 1 1 0 0;0 0 1 1 0')
# a = generate_test.generate(10, 10, 4)
# a = np.matrix('1 1 0 0 0;0 1 1 0 0;0 0 1 1 0;0 0 0 1 1;1 0 0 0 1')
# print(a)
# print(dir(a))
# np.save('F.npy', a)

# F = np.load('F.npy')
tme = time.time()
F = generate_test.generate(n, p, k)
tme = time.time() - tme
print(F)
print("Time taken to generate matrix : ", tme)
C = F.sum(1)
p = C.size
# print(F.dtype)
n = F.size // p

print("n=%d, p=%d, k=%d" % (n, p, k))

k = [k] * n
k = np.array(k)


def z(x):
    if type(x) == type(list):
        return (C.T.dot(np.array(x))).item(0)
    else:
        return (C.T.dot(x)).item(0)


def feasible(x):
    mysol = np.array(x)
    tru = (F.T.dot(mysol))
    tru = np.array(tru.tolist()[0])
    tru = tru >= k
    tru = tru.tolist()
    satisfied = True
    for v in tru:
        satisfied = satisfied and v
    return satisfied


# print(feasible([0]))

# print(feasible([0, 1, 0, 0, 0, 0, 0, 1, 0, 0]))


def main_checker(x):
    # if z(x) > z(parent):
    #     return False
    future_sol = x[:depth + 1]
    future_sol = future_sol + [1] * (p - depth - 1)
    # print(future_sol)
    return feasible(future_sol) and not feasible(x)


def isMin(x):
    if z(x) <= minimum_value:
        return z(x)
    return minimum_value


stack = [[[0] * p, -1]]

parent = []
wasInStack = [[0] * p]
iterations = 0
depth = -1
minimum_value = math.inf

tme = time.time()
while stack:
    parent, depth = stack.pop()
    stack_size = len(stack)
    depth += 1
    left_sol = parent[:]
    left_sol[depth] = 0
    # print("depth = ", depth)
    try:
        left_sol[depth + 1] = 1
        # print("l : ", left_sol)

        if main_checker(left_sol) and z(left_sol)<minimum_value:
            stack.append([left_sol, depth])
        elif feasible(left_sol):
            # print(left_sol)
            minimum_value = isMin(left_sol)
            solutions.append(left_sol)

            # depth -= 1

    except IndexError:
        pass
    right_sol = parent[:]
    right_sol[depth] = 1

    # print("r : ", right_sol)
    if main_checker(right_sol) and z(right_sol)<minimum_value:
        stack.append([right_sol, depth])
    elif feasible(right_sol):
        # print(right_sol)
        minimum_value = isMin(right_sol)
        solutions.append(right_sol)
        # depth -= 1
    # print("stack : ", stack)

    # if stack_size == len(stack):
    #     depth -= 1

    # print("sol : ", solutions)
    iterations += 1
    # print("\ni :", iterations)
    # if iterations > 32:
    #     break
tme = time.time() - tme
print("\nMinimum Value : ", minimum_value)

print("\nSolutions : ")
unique_solutions = [list(x) for x in set(tuple(x) for x in solutions)]
for i in solutions:
    if z(i) == minimum_value:
        print(i)
print("\nNumber of Iterations : ", iterations)
print("\nTime Taken :", tme)
# print(x.dtype)
# print(x.astype(int))
# print(C)
# print(Z(x.T))
