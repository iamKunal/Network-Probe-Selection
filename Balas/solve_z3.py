#!/usr/bin/env python


from z3 import *
import numpy as np
import generate_test


n,p,k = map(int, raw_input().split())

F = generate_test.generate(n,p,k)

opt = Optimize()

C=F.sum(1)

