import matplotlib.pyplot as plt
import numpy as np

x = [0.] * 32
x[-1] = 1.

plt.plot(x, 'rs-', label='initialization')

for iter in range(512):
    for i in range(1, len(x)-1):
        x[i] = ( x[i-1] + x[i+1] - (i+31)/31**3 )/2.

plt.plot(x, 'bs-', label='smoothed data')

# plot the ground truth
X = np.linspace(0., 1., num=32, endpoint=True)
G = [x**3/6 + x**2/2 + x/3 for x in X]
plt.plot(G, 'g-', label='ground truth')

plt.legend()
plt.show()

