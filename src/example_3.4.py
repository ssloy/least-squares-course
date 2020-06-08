import matplotlib.pyplot as plt
import numpy as np

# initialize the data array
x = [0, .8, 1, .6, .1, .4, .2, .1, .6, .3, 1, .7, .4, 0, .6, 1]

plt.plot(x, 'rs-', label='initialization')

# smooth the array values
for iter in range(100):
    for i in range(1, len(x)-1):
        x[i] = ( x[i-1] + x[i+1] - (i+15)/15**3 )/2.

plt.plot(x, 'bs-', label='cubic function')

# plot the ground truth
X = np.linspace(0., 1., num=16, endpoint=True)
G = [x**3/6 + x**2/2 + x/3 for x in X]
plt.plot(G, 'g-', label='ground truth')

plt.legend()
plt.show()
