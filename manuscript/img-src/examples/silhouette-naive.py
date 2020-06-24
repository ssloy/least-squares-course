import numpy as np
import matplotlib.pyplot as plt

x = [100,100,97,93,91,87,84,83,85,87,88,89,90,90,90,88,87,86,84,82,80,
     77,75,72,69,66,62,58,54,47,42,38,34,32,28,24,22,20,17,15,13,12,9,
     7,8,9,8,6,0,0,2,0,0,2,3,2,0,0,1,4,8,11,14,19,24,27,25,23,21,19]
y = [0,25,27,28,30,34,37,41,44,47,51,54,59,64,66,70,74,78,80,83,86,90,93,
     95,96,98,99,99,100,99,99,99,98,98,96,94,93,91,90,87,85,79,75,70,65,
     62,60,58,52,49,46,44,41,37,34,30,27,20,17,15,16,17,17,19,18,14,11,6,4,1]
n = len(x)

plt.plot(x+[x[0]], y+[y[0]], 'g--')

cx = [x[i] - (x[(i-1+n)%n]+x[(i+1)%n])/2 for i in range(n)]
cy = [y[i] - (y[(i-1+n)%n]+y[(i+1)%n])/2 for i in range(n)]

for iter in range(100):
    for i in range(n):
        x[i] = (x[(i-1+n)%n]+x[(i+1)%n])/2 + cx[i]*1.9
        y[i] = (y[(i-1+n)%n]+y[(i+1)%n])/2 + cy[i]*1.9

plt.plot(x+[x[0]], y+[y[0]], 'k-', linewidth=3)
plt.xlim(-40, 160)
plt.ylim(-60, 140)
plt.axis('off')
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('silhouette-naive-100.png', bbox_inches='tight')
plt.show()

