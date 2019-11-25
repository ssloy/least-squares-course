# initialize the data array
x = [0.] * 32
x[0] = x[31] = 1.
x[18] = 2.

# smooth the array values other than at indices 0,18,31
for iter in range(128):
    for i in range(0, len(x)):
        if i in [0,18,31]: continue
        x[i] = (x[i-1]+x[i+1])/2.
