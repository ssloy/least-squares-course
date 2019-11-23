import numpy as np
import matplotlib.pyplot as plt

n = 32 # size of the vector to produce
m = 18 # index of the element constrained to be = 2

# the matrix will have the size (n-3) x (n-3),
# but it is easier to fill the pattern with n x n first
A = np.matrix(np.zeros((n, n)))
for i in range(1,n-2): # fill the matrix with 2nd order finite differences
    A[i, i-1] = -1.
    A[i, i]   =  2.
    A[i, i+1] = -1.

A = A[1:-2,1:-2] # remove constrained variables from the system
A[m-2,m-1] = 0
A[m-1,m-2] = 0

b = np.matrix(np.zeros((n-3, 1))) # initialize the right hand side with zeros

# put the constrained variables to the right hand side
b[0,0]   = 1.
b[m-2,0] = 2.
b[m-1,0] = 2.
b[-1,0]  = 1.

# solve the system
x = (np.linalg.inv(A)*b).transpose().tolist()[0]

# re-introduce constrained variables
x.insert(0, 1.)
x.insert(m, 2.)
x.append(1.)

# plot the solution
plt.plot(x, 'bs-', label='smoothed data')
plt.show()

