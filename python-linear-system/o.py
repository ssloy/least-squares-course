import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True,linewidth=np.nan,threshold=np.nan)

n = 32 # size of the vector to produce

# fill the matrix with 2nd order finite differences
A = np.matrix(np.zeros((n-1+3, n)))
for i in range(0,n-1):
    A[i, i]   = -1.
    A[i, i+1] =  1.

# enforce the constraints through the quadratic penalty
A[n-1+0, 0] = 1.
A[n-1+1,18] = 1.
A[n-1+2,31] = 1.

b = np.matrix(np.zeros((n-1+3, 1)))
b[n-1+0,0] = 1.
b[n-1+1,0] = 2.
b[n-1+2,0] = 1.

# solve the system
x = np.linalg.inv(A.transpose()*A)*A.transpose()*b
x = x.transpose().tolist()[0]

# plot the solution
plt.plot(x, 'bs-', label='smoothed data')
plt.show()

