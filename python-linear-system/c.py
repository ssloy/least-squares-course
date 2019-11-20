import matplotlib.pyplot as plt

# initialize the data array
x = [0.] * 32
x[0] = x[31] = 1.
x[18] = 2.

c = 11./32**2

plt.plot(x, 'rs-', label='initialization')

# smooth the array values other than at indices 0,18,31
for iter in range(1000):
    for i in range(len(x)):
        if i in [0,18,31]: continue
        x[i] = (x[i-1]+x[i+1]+c)/2.

plt.plot(x, 'bs-', label='prescribed curvature + constraints')
plt.legend()
plt.show()

