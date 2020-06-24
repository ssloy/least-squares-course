import numpy as np

fa = 1 # left constraint
fb = 3 # right constraint
n = 40
x = np.linspace(0, 2*np.pi, n)
g = [np.sin(p) for p in x]

A = np.matrix(np.zeros((n-1,n-2)))
b = np.matrix(np.zeros((n-1,1)))
A[0,0]      =  1
b[0,0]      =  fa + g[1]-g[0]
A[n-2, n-3] = -1
b[n-2,0]    = -fb + g[-1]-g[-2]
for i in range(1,n-2):
    b[i,0] = g[i]-g[i-1]
    A[i, i-1] = -1
    A[i, i  ] =  1

f = [fa] + (np.linalg.inv(A.T*A)*A.T*b).T.tolist()[0] + [fb]

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)
#plt.rc('axes', titlesize=20, labelsize=20)
#plt.rc('xtick', labelsize=40)    # fontsize of the tick labels

fig,ax = plt.subplots(1, figsize=(6.40,6.40),dpi=150)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(20)


plt.plot(x, f, linewidth=3, label='$f(x)$')
plt.plot(x, g, linewidth=3, label='$g(x) = \sin x$')
plt.scatter([x[0], x[-1]], [fa,fb], color='red', edgecolors='black',s=200)
plt.legend(frameon=False)
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
#plt.savefig('prepie.png', bbox_inches='tight')
plt.show()
