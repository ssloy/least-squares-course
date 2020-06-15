import numpy as np

X = [0.2,37.9,32.0,12.7,23.3,8.2,25.2,27.0,40.9,4.7,19.1,50.7,53.2,59.3,15.2,45.5]
Y = [0.04,4.79,4.51,0.30,3.05,0.01,3.61,4.14,4.77,0.01,1.64,4.77,4.56,4.53,0.67,4.61]
n = len(X)

guess_c = np.max(Y)*1.1 # 1.1 to avoid division by zero

A = np.matrix(np.zeros((n, 2)))
b = np.matrix(np.zeros((n, 1)))
for i in range(n):
    A[i,0] = 1
    A[i,1] = X[i]
    b[i,0] = np.log(Y[i]/(guess_c - Y[i]))

guess_w0, guess_w = (np.linalg.inv(A.T*A)*A.T*b).T.tolist()[0]


U = np.matrix([[guess_c],[guess_w0],[guess_w]])
for _ in range(5):
    JR = np.matrix(np.zeros((n, 3)))
    R  = np.matrix(np.zeros((n, 1)))
    for i in range(n):
        ei = np.exp(-U[1,0] - X[i]*U[2,0])
        R[i,0] = U[0,0]/(1+ei) - Y[i]
        for j in range(3):
            JR[i, 0] = 1/(1+ei)
            JR[i, 1] = U[0,0]*ei/(1+ei)**2
            JR[i, 2] = X[i]*U[0,0]*ei/(1+ei)**2
    U = U - np.linalg.inv(JR.T*JR)*JR.T*R


import matplotlib.pyplot as plt
plt.scatter(X,Y, color='red', edgecolors='black')

def sigmoid(x, c,w0,w):
    return c/(1+np.exp(-w*x-w0))

fit_x = np.linspace(np.min(X), np.max(X), num=100)
fit_y = sigmoid(fit_x, guess_c, guess_w0, guess_w)
plt.plot(fit_x, fit_y)
fit_y = sigmoid(fit_x, U[0,0], U[1,0], U[2,0])
plt.plot(fit_x, fit_y)

plt.show()

