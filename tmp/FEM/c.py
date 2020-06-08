import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
#plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)
fig, ax = plt.subplots(1, figsize=(6.40,6.40),dpi=100)

#rhs:radcan(radcan(integrate(n*(x-(i-1)/n)*(x+1),x,(i-1)/n,i/n)) + radcan(integrate(n*((i+1)/n-x)*(x+1),x,i/n,(i+1)/n)));

# initialize the data array
n = 3
phi = [0.]*(n+1)
phi[0] = 0
phi[n] = 1

# solve the linear system
for iter in range(1000):
    for i in range(1,n):
        rhs = (n+i)/n**3
        phi[i] = (phi[i-1] + phi[i+1] - rhs)/2.

# plot the solution
plt.plot(np.linspace(0., 1., n+1), phi, 'gs-', label='FEM solution')

# plot the ground truth
X = np.linspace(0., 1., 100)
G = [x**3/6 + x**2/2 + x/3 for x in X]
plt.plot(X, G, 'r-', label='ground truth')

plt.legend()
plt.show()

