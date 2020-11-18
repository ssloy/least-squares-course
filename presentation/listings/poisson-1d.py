import numpy as np
n,f0,fn = 32,1.,3.
g = [np.sin(x) for x in np.linspace(0, 2*np.pi, n)]
A = np.matrix(np.zeros((n-1,n-2)))
np.fill_diagonal(A,      1)
np.fill_diagonal(A[1:], -1)
b = np.matrix([[g[i]-g[i-1]] for i in range(1,n)])
b[ 0,0] = b[ 0,0] + f0
b[-1,0] = b[-1,0] - fn
f = [f0] + (np.linalg.inv(A.T*A)*A.T*b).T.tolist()[0] + [fn]
