import numpy as np
n,f0,fn = 32,1.,3.
g = [np.sin(x) for x in np.linspace(0, 2*np.pi, n)]
f = [f0] + [0]*(n-2) + [fn]
for _ in range(512):
    for i in range(1, n-1):
        f[i] = ( f[i-1] + f[i+1] + (2*g[i]-g[i-1]-g[i+1]) )/2.

import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)
fig,ax = plt.subplots(1, figsize=(6.40,6.40),dpi=150)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(20)
x = np.linspace(0, 2*np.pi, n)
plt.plot(x, f, linewidth=3, label='$f(x)$')
plt.plot(x, g, linewidth=3, label='$g(x) = \sin x$')
plt.scatter([x[0], x[-1]], [f0,fn], color='red', edgecolors='black',s=200)
plt.legend(frameon=False)
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
#plt.savefig('prepie.png', bbox_inches='tight')
plt.show()
