# initialize the data array
x = [0.] * 32
x[31] = 1.

# smooth the array values
for iter in range(128):
    for i in range(1, len(x)-1):
        x[i] = (x[i-1]+x[i+1])/2.
