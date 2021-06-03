import numpy as np
X = [0.2,37.9,32.0,12.7,23.3,8.2,25.2,27.0,
     40.9,4.7,19.1,50.7,53.2,59.3,15.2,45.5]
Y = [0.04,4.79,4.51,0.30,3.05,0.01,3.61,4.14,
     4.77,0.01,1.64,4.77,4.56,4.53,0.67,4.61]
c = np.max(Y)+0.01 # +eps to avoid division by zero
A = np.matrix(np.column_stack(([1.]*len(X), X)))
b = np.matrix([np.log(y/(c-y)) for y in Y]).T
print(np.linalg.inv(A.T*A)*A.T*b)
