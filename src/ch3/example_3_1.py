import matplotlib.pyplot as plt

# initialize the data array
x = [0, .8, 1, .6, .1, .4, .2, .1, .6, .3, 1, .7, .4, 0, .6, 1]

plt.plot(x, 'rs-', label='initialization')

# smooth the array values
for iter in range(512):
    x = [ x[0] ] + [ (x[i-1]+x[i+1])/2. for i in range(1, len(x)-1) ] + [ x[-1] ]

plt.plot(x, 'bs-', label='smoothed data')
plt.legend()
plt.show()
