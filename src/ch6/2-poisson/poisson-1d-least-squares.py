import numpy as np
n,f0,fn = 32,1.,3.
g = [np.sin(x) for x in np.linspace(0, 2*np.pi, n)]
A = np.matrix(np.zeros((n-1,n-2)))
np.fill_diagonal(A,      1)
np.fill_diagonal(A[1:], -1)
b = np.matrix([[g[i]-g[i-1]] for i in range(1,n)])
b[ 0,0] = b[ 0,0] + f0
b[-1,0] = b[-1,0] - fn
f = [f0] + (np.linalg.inv(A.T*A)*A.T*b).T.tolist()[0] + [fn]

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
