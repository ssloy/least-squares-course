import numpy as np
n,v0,vn = 30,0.5,2.3
A = np.matrix(np.vstack((np.diag([1]*n), [1]*n)))
b = np.matrix([[0]]*n + [[vn-v0]])
u = np.linalg.inv(A.T*A)*A.T*b
v = [v0 + np.sum(u[:i]) for i in range(0,n+1)]

import matplotlib.pyplot as plt
plt.plot(v, 'bs-', label='v(t)')
plt.plot(u, 'gs-', label='u(t)')
plt.legend(frameon=False)
plt.show()
