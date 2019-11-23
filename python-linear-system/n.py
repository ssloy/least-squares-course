import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True,linewidth=np.nan,threshold=np.nan)

n = 32 # size of the vector to produce

# fill the matrix with 2nd order finite differences
A = np.matrix(np.zeros((n-1, n)))
for i in range(0,n-1):
    A[i, i]   = -1.
    A[i, i+1] =  1.

# eliminate the constrained variables from the matrix
A = A[:,[*range(1,18)] + [*range(19,31)]]

b = np.matrix(np.zeros((n-1, 1)))
b[0,0]   =  1.
b[17,0] = -2.
b[18,0]   =  2.
b[n-2,0] = -1.

# solve the system
x = np.linalg.inv(A.transpose()*A)*A.transpose()*b
x = x.transpose().tolist()[0]

# re-introduce the constrained variables
x.insert(0, 1.)
x.insert(18, 2.)
x.append(1.)

# plot the solution
plt.plot(x, 'bs-', label='smoothed data')
plt.show()

