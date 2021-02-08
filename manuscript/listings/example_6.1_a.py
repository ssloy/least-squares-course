import numpy as np
n,v0,vn = 30,0.5,2.3
A = np.matrix(np.tril(np.ones((n,n))))
b = np.matrix([[vn-v0]]*n)
u = np.linalg.inv(A.T*A)*A.T*b
v = [v0 + np.sum(u[:i]) for i in range(0,n+1)]
