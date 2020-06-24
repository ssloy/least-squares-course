import numpy as np
import matplotlib.pyplot as plt

n = 30
A = np.matrix(np.zeros((2*n, n)))
b = np.matrix(np.zeros((2*n, 1)))

for i in range(0,n): # x_i = 2.3
    for j in range(0,i+1):
        A[i, j] = 1
    b[i, 0] = 2.3 - 0.5
for i in range(0,n): # u_i = 0
    A[n+i, i] = 1*2.

u = np.linalg.inv(A.T*A)*A.T*b
v = [.5 + np.sum(u[:i]) for i in range(0,n+1)]

plt.plot(v, 'bs-', label='v(t)')
plt.plot(u, 'gs-', label='u(t)')
plt.legend(frameon=False)
plt.show()
