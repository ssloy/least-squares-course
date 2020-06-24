import numpy as np
import matplotlib.pyplot as plt

logistic = False
samples = [[0.47,1],[0.24,1],[0.75,1],[0.00,1],[-0.80,1],[-0.59,1],[1.09,1],[1.34,1],
           [1.01,1],[-1.02,1],[0.50,1],[0.64,1],[-1.15,1],[-1.68,1],[-2.21,1],[-0.52,1],
           [3.93,1],[4.21,1],[5.18,1],[4.20,1],[4.57,1],[2.63,1],[4.52,1],[3.31,1],
           [6.75,1],[3.47,1],[4.32,1],[3.08,1],[4.10,1],[4.00,1],[2.99,1],[3.83,1]]
n = len(samples)
m = len(samples[0])
labels = [0]*(n//2) + [1]*(n//2)

k = 100

X = []
Y = []
Z = []
a,b = -8.132648217846736, 4.07391337959378
for x in np.linspace(a-3,a+17,k):
    for y in np.linspace(b-13,b+7,k):
        E = 0
        for i in range(n):
            if logistic:
                E -= labels[i]*(+samples[i][0]*y + x) - np.log(1+np.exp(+x + samples[i][0]*y)) - 0.001*(x**2 + y**2)
            else:
#                E += (labels[i] - 1/(1+np.exp(-x - samples[i][0]*y)))**2 + 0.001*(x**2 + y**2)
                E += (labels[i] - 1/(1+np.exp(-x - samples[i][0]*y)))**2
        print("v %3.3f %3.3f %3.3f" %(x,y,E))
        X.append(x)
        Y.append(y)
        Z.append(E)

for i in range(k-1):
    for j in range(k-1):
        print("f %d %d %d %d" %(i+j*k+1, i+1+j*k+1, i+1+(j+1)*k+1, i+(j+1)*k+1) )


'''
X, Y = np.meshgrid(X, Y)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X,Y,Z)
plot.show()
'''
