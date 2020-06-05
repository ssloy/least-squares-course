import matplotlib.pyplot as plt

x = [0.] * 32
x[-1] = 1.

plt.plot(x, 'rs-', label='initialization')

for iter in range(512):
    for i in range(1, len(x)-1):
        x[i] = ( x[i-1] + x[i+1] - (i+31)/31**3 )/2.

plt.plot(x, 'bs-', label='smoothed data')

plt.legend()
plt.show()

