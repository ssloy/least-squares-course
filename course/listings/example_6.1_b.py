import numpy as np

n = 30
A = np.matrix(np.zeros((n+1, n)))
b = np.matrix(np.zeros((n+1, 1)))

b[0, 0] = 2.3 - 0.5
for i in range(0,n):
    A[0,   i] = 1 # x_n = 2.3
    A[1+i, i] = 1 # u_i = 0

u = np.linalg.inv(A.T*A)*A.T*b
v = [.5 + np.sum(u[:i]) for i in range(0,n+1)]
