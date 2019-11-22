import numpy as np
import matplotlib.pyplot as plt

#rhs:radcan(radcan(integrate(n*(x-(i-1)/n)*(x+1),x,(i-1)/n,i/n)) + radcan(integrate(n*((i+1)/n-x)*(x+1),x,i/n,(i+1)/n)));

# right hand side
def rhs(n, i):
    if (i==n-1):
        return -(n+i)/n**2 + n
    return -(n+i)/n**2

# initialize the data array
n = 3
x = [0.] * (n+1)
x[0] = 0
x[n] = 1


for iter in range(1000):
    for i in range(1,n):
        c = rhs(n,i)/n
        print(i, c)
        x[i] = (x[i-1]+x[i+1] - c)/2.


plt.plot([0,1/3, 2/3, 1], x, 'bs-', label='prescribed curvature + constraints')
plt.legend()


T = np.arange(0,1,.01)
G = []
for t in T:
    G.append(t**3/6 + t**2/2 + t/3)

plt.plot(T, G)
plt.show()

