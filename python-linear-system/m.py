import numpy as np
import matplotlib.pyplot as plt

n = 16 # size of the vector to produce

# the matrix will have the size (n-2) x (n-2),
# but it is easier to fill the pattern with (n-2) x n first
A = np.matrix(np.zeros((n-2, n)))
for i in range(1,n-1): # fill the matrix with 2nd order finite differences
    A[i-1, i-1] = -1.
    A[i-1, i]   =  2.
    A[i-1, i+1] = -1.
A = A[:,1:-1] # eliminate the constrained variables from the system

b = np.matrix(np.zeros((n-2, 1))) # initialize the right hand side with zeros
b[0,0]   = 0. # add the constrained variables to the right hand side
b[-1,0]  = 1.

# solve the system
x = (np.linalg.inv(A)*b).transpose().tolist()[0]

# re-introduce the constrained variables
x.insert(0, 0.)
x.append(1.)

# plot the solution
plt.plot(x, 'bs-', label='smoothed data')
plt.show()

