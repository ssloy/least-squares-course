import numpy as np
samples = [[0.47,1],[0.24,1],[0.75,1],[0.00,1],[-0.80,1],[-0.59,1],[1.09,1],[1.34,1],
           [1.01,1],[-1.02,1],[0.50,1],[0.64,1],[-1.15,1],[-1.68,1],[-2.21,1],[-0.52,1],
           [3.93,1],[4.21,1],[5.18,1],[4.20,1],[4.57,1],[2.63,1],[4.52,1],[3.31,1],
           [6.75,1],[3.47,1],[4.32,1],[3.08,1],[4.10,1],[4.00,1],[2.99,1],[3.83,1]]
n = len(samples)
m = len(samples[0])
labels = [0]*(n//2) + [1]*(n//2)

W = np.matrix([[1],[1]])
for _ in range(5):
    JR = np.matrix(np.zeros((n+2, 2)))
    R  = np.matrix(np.zeros((n+2, 1)))
    for i in range(n):
        ei = np.exp(-W[1,0] - samples[i][0]*W[0,0])
        R[i,0] = -1/(1+ei) + labels[i]
        for j in range(3):
            JR[i, 0] = samples[i][0]*ei/(1+ei)**2
            JR[i, 1] = ei/(1+ei)**2
    l = .001 # regularization
    JR[n,0] = JR[n+1, 1] = 1.*l
    R[n  ,0] = -W[0]*l
    R[n+1,0] = -W[1]*l
    W = W + np.linalg.inv(JR.T*JR)*JR.T*R
