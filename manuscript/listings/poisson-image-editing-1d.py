import numpy as np

fa = 1 # left constraint
fb = 3 # right constraint
n = 40
x = np.linspace(0, 2*np.pi, n)
g = [np.sin(p) for p in x]

A = np.matrix(np.zeros((n-1,n-2)))
b = np.matrix(np.zeros((n-1,1)))
A[0,0]      =  1
b[0,0]      =  fa + g[1]-g[0]
A[n-2, n-3] = -1
b[n-2,0]    = -fb + g[-1]-g[-2]
for i in range(1,n-2):
    b[i,0] = g[i]-g[i-1]
    A[i, i-1] = -1
    A[i, i  ] =  1

f = [fa] + (np.linalg.inv(A.T*A)*A.T*b).T.tolist()[0] + [fb]
