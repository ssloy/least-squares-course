import numpy as np
n,v0,vn = 30,0.5,2.3
A = np.matrix(np.vstack((np.tril(np.ones((n,n))), np.diag([2]*n))))
b = np.matrix([[vn-v0]]*n + [[0]]*n)
u = np.linalg.inv(A.T*A)*A.T*b
v = [v0 + np.sum(u[:i]) for i in range(0,n+1)]

import matplotlib.pyplot as plt
plt.plot(v, 'bs-', label='v(t)')
plt.plot(u, 'gs-', label='u(t)')
plt.legend(frameon=False)
plt.show()
