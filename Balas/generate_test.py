from z3 import *
import numpy as np


def generate(N, P, k):
    solver = Solver()
    F = [[z3.Int('f_%d_%d' % (p, n)) for n in range(N)] for p in range(P)]
    percentage = math.ceil(0.2 * N)
    for n in range(N):
        solver.add(z3.Sum([F[p][n] for p in range(P)]) >= k + 1)
    for p in range(P):
        solver.add(z3.Sum([F[p][n] for n in range(N)]) >= percentage)
    for n in range(N):
        for p in range(P):
            solver.add(F[p][n] <= 1)
            solver.add(F[p][n] >= 0)
    solver.check()
    m = solver.model()
    mat = []
    for p in range(P):
        cur = []
        for n in range(N):
            cur.append(m[F[p][n]].as_long())
        mat.append(cur[:])
    return np.matrix(mat)
