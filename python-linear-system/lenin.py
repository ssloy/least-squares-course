import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

def amplify(x):
    n = len(x)
    A = np.matrix(np.zeros((n+(n-2),n)))
    b = np.matrix(np.zeros((n+(n-2),1)))

    row = 0
    for i in range(0,n):
        scale = 10. if i==0 or i==n-1 else .1
        A[row, i] =   1.*scale
        b[row, 0] = x[i]*scale
        row += 1

    for i in range(1,n-1):
        A[row, i] = 2.
        A[row, i-1] = -1.
        A[row, i+1] = -1.
        b[row, 0] = 1.9*(2.*x[i] - x[i-1] - x[i+1])
        row += 1

    return np.linalg.inv(A.T*A)*A.T*b

in_x = [100,100,97,93,91,87,84,83,85,87,88,89,90,90,90,88,87,86,84,82,80,
     77,75,72,69,66,62,58,54,47,42,38,34,32,28,24,22,20,17,15,13,12,9,
     7,8,9,8,6,0,0,2,0,0,2,3,2,0,0,1,4,8,11,14,19,24,27,25,23,21,19]
in_y = [0,25,27,28,30,34,37,41,44,47,51,54,59,64,66,70,74,78,80,83,86,90,93,
     95,96,98,99,99,100,99,99,99,98,98,96,94,93,91,90,87,85,79,75,70,65,
     62,60,58,52,49,46,44,41,37,34,30,27,20,17,15,16,17,17,19,18,14,11,6,4,1]

out_x = amplify(in_x)
out_y = amplify(in_y)

ax.plot(x,y,'bs-')
ax.plot(out_x, out_y)

plt.show()
