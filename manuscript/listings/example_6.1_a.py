import numpy as np

n = 30
A = np.matrix(np.zeros((n, n)))
b = np.matrix(np.zeros((n, 1)))

for i in range(0,n): # x_i = 2.3
    for j in range(0,i+1):
        A[i, j] = 1
    b[i, 0] = 2.3 - 0.5

u = np.linalg.inv(A.T*A)*A.T*b
v = [.5 + np.sum(u[:i]) for i in range(0,n+1)]
