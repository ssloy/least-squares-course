import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=30)
fig, ax = plt.subplots(1, figsize=(6.40,6.40),dpi=100)



def w(x, e, i, n):
    if x<(i-1)/n-e:
        return 0
    if x<(i-1)/n+e:
        return (n*x+e*n-i+1)**2/(4*e*n)
    if x<i/n-e:
        return n*x-i+1
    if x<i/n+e:
        return (1-(n*x-i)**2-(n*e-1)**2)/(2*e*n)
    if x<(i+1)/n-e:
        return i+1-n*x
    if x<(i+1)/n+e:
        return (n*x-e*n-i-1)**2/(4*e*n)
    return 0

i = 1
e=0.05
n = 3

X  = np.linspace((i-1)/n-e, (i-1)/n+e, num=100, endpoint=True)
W = [w(x,e,i,n) for x in X]
plt.plot(X, W, 'r-', linewidth=3)

X  = np.linspace((i-1)/n+e,i/n-e, num=100, endpoint=True)
W = [w(x,e,i,n) for x in X]
plt.plot(X, W, 'g-', linewidth=3)

X  = np.linspace(i/n-e, i/n+e, num=100, endpoint=True)
W = [w(x,e,i,n) for x in X]
plt.plot(X, W, 'r-', linewidth=3)

X  = np.linspace(i/n+e, (i+1)/n-e, num=100, endpoint=True)
W = [w(x,e,i,n) for x in X]
plt.plot(X, W, 'g-', linewidth=3)

X  = np.linspace((i+1)/n-e, (i+1)/n+e, num=100, endpoint=True)
W = [w(x,e,i,n) for x in X]
plt.plot(X, W, 'r-', linewidth=3)


plt.tight_layout()
#plt.gca().axes.get_yaxis().set_visible(False)
#plt.gca().axes.get_xaxis().set_visible(False)
plt.ylim(0., 1.)
plt.xlim(-e, 1.)

plt.savefig("convolution.png", bbox_inches='tight')
plt.show()

