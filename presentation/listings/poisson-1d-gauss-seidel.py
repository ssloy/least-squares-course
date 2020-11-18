import numpy as np
n,f0,fn = 32,1.,3.
g = [np.sin(x) for x in np.linspace(0, 2*np.pi, n)]
f = [f0] + [0]*(n-2) + [fn]
for _ in range(512):
    for i in range(1, n-1):
        f[i] = ( f[i-1] + f[i+1] + (2*g[i]-g[i-1]-g[i+1]) )/2.
