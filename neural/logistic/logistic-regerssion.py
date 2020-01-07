import matplotlib.pyplot as plt
import numpy as np
import math

# c = carrying capacity
def sigmoid(x, c,w0,w):
    return c/(1+np.exp(-w*x-w0))

X = [0.2, 37.9, 32.0, 12.7, 23.3, 8.2, 25.2, 27.0, 40.9, 4.7, 19.1, 50.7, 53.2, 59.3, 15.2, 45.5]
Y = [0.04, 4.79, 4.51, 0.30, 3.05, 0.01, 3.61, 4.14,  4.77, 0.01, 1.64, 4.77, 4.56, 4.53, 0.67, 4.61]

n = len(X)
guess_c = np.max(Y)*1.1

A = np.matrix(np.zeros((n, 2)))
b = np.matrix(np.zeros((n, 1)))

for i in range(n):
    A[i,0] = 1
    A[i,1] = X[i]
    b[i,0] = math.log(Y[i]/(guess_c - Y[i]))

guess_w0, guess_w = (np.linalg.inv(A.T*A)*A.T*b).T.tolist()[0]

plt.scatter(X,Y, color='red', edgecolors='black')

fit_x = np.linspace(np.min(X), np.max(X), num=100)
fit_y = sigmoid(fit_x, guess_c, guess_w0, guess_w)
plt.plot(fit_x, fit_y)

plt.show()

