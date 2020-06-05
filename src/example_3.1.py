import matplotlib.pyplot as plt

# initialize the data array
x = [-1] * 32
x[0] = 0.
x[-1] = 1.

plt.plot(x, 'rs-', label='initialization')

# smooth the array values
for iter in range(10000):
    for i in range(1, len(x)-1):
        x[i] = ( x[i-1] + x[i+1] )/2.
    x[-1] = x[-2]

plt.plot(x, 'bs-', label='smoothed data')

plt.legend()
plt.show()

