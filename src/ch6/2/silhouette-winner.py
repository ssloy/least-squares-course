import numpy as np
import matplotlib.pyplot as plt

x = [100,100,97,93,91,87,84,83,85,87,88,89,90,90,90,88,87,86,84,82,80,
     77,75,72,69,66,62,58,54,47,42,38,34,32,28,24,22,20,17,15,13,12,9,
     7,8,9,8,6,0,0,2,0,0,2,3,2,0,0,1,4,8,11,14,19,24,27,25,23,21,19]
y = [0,25,27,28,30,34,37,41,44,47,51,54,59,64,66,70,74,78,80,83,86,90,93,
     95,96,98,99,99,100,99,99,99,98,98,96,94,93,91,90,87,85,79,75,70,65,
     62,60,58,52,49,46,44,41,37,34,30,27,20,17,15,16,17,17,19,18,14,11,6,4,1]
n = len(x)

A = np.matrix(np.zeros((4+2*n,2*n)))
b = np.matrix(np.zeros((4+2*n,1)))
for i in range(0, n):
    j, k = (i+1)%n, (i+2)%n
    PR     = [x[k]-x[i], y[k]-y[i]]
    PQ     = [x[j]-x[i], y[j]-y[i]]
    PRperp = [y[i]-y[k], x[k]-x[i]]
    c0 = np.dot(PQ, PR    )/np.dot(PR, PR)
    c1 = np.dot(PQ, PRperp)/np.dot(PR, PR)*1.3

    A[i*2, i*2  ] =  1-c0
    A[i*2, j*2  ] = -1
    A[i*2, k*2  ] =  c0
    A[i*2, k*2+1] = -c1
    A[i*2, i*2+1] =  c1

    A[i*2+1, i*2+1] =  1-c0
    A[i*2+1, j*2+1] = -1
    A[i*2+1, k*2+1] =  c0
    A[i*2+1, k*2  ] =  c1
    A[i*2+1, i*2  ] = -c1

lock1 = 9123%n # pin two arbitrary points
lock2 = 3478%n

A[n*2, lock1*2] = A[n*2+1, lock1*2+1] = A[n*2+2, lock2*2] = A[n*2+3, lock2*2+1] = 10.
b[-1] = y[lock2]*10.
b[-2] = x[lock2]*10.
b[-3] = y[lock1]*10.
b[-4] = x[lock1]*10.

X = (np.linalg.inv(A.T*A)*A.T*b).tolist()

plt.plot(x+[x[0]], y+[y[0]], 'g--')
plt.plot(X[::2]+[X[0]], X[1::2]+[X[1]], 'k-', linewidth=3)
plt.axis('off')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

