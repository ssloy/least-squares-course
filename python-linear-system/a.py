import matplotlib.pyplot as plt

# initialize the data array
x = [0.] * 32
x[0] = x[31] = 1.
x[18] = 2.

plt.plot(x, 'rs-', label='initialization')

# smooth the array values
for iter in range(1000):
    x[0] = x[1]
    for i in range(1, len(x)-1):
        x[i] = (x[i-1]+x[i+1])/2.
    x[-1] = x[-2]

plt.plot(x, 'bs-', label='smoothed data')
plt.legend()
plt.show()

