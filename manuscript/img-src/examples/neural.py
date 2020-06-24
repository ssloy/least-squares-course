import numpy as np

samples = [[.5,.7,1.],[.1,.5,1.],[.3,.6,1.],[.2,.8,1.],[.17,.17,1.],[.2,.3,1.],
           [.3,.4,1.],[.05,.2,1.], [.2,.3,1.],[.8,.3,1.],[.5,.2,1.],[.7,.2,1.],
           [.9,.1,1.],[.8,.4,1.],[.6,.5,1.], [.5,.4,1.], [.9, .5, 1.],[.79, .6, 1.],
           [.73, .7, 1.],[.9, .8, 1.],[.95, .4, 1.]]
labels = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0]

def neuron(x, w):
    return 1./(1.+np.exp(-np.dot(x,w)))

u = np.array([0.814, 0.779, 0.103]) # small random values
v = np.array([0.562, 0.310, 0.591])
w = np.array([0.884, 0.934, 0.649])

alpha = 1. # learning rate
for _ in range(0,3000):
    E = 0
    for x, label in zip(samples,labels):
        E += (label - neuron([neuron(x, u), neuron(x, v), 1.],w))**2
    print("E =",E)

    for x, label in zip(samples,labels):
        out_u = neuron(x, u)
        out_v = neuron(x, v)
        out_w = neuron([out_u, out_v, 1.], w)
        u += alpha*(label-out_w)*out_w*(1.-out_w)*out_u*(1.-out_u)*np.array(x)
        v += alpha*(label-out_w)*out_w*(1.-out_w)*out_v*(1.-out_v)*np.array(x)
        w += alpha*(label-out_w)*out_w*(1.-out_w)*np.array([out_u, out_v, 1.])

#print(u,v,w)

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)

fig,ax = plt.subplots(1, figsize=(6.40*1.25,6.40),dpi=150)

res = 100
x0 = np.arange(0, 1., 1./res)
x1 = np.arange(0, 1., 1./res)

Y = [[neuron([neuron([a,b,1.], u), neuron([a,b,1],v), 1.], w) for a in x0] for b in x1]


X0, X1 = np.meshgrid(x0, x1)
#print(X0, X1, Y)
plt.contourf(X0, X1, Y,100, cmap=plt.cm.RdYlGn)
plt.colorbar()
plt.contour(X0, X1, Y,levels=[.49995, .50005], colors='k', linestyles='--')

for sample, label in zip(samples,labels):
    c = 'lime'
    if (label<.5): c = 'tomato'
    plt.scatter(sample[0], sample[1], color=c, edgecolors='black',s=200,linewidths=2)

plt.tight_layout()
plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)
plt.savefig("neural.png", bbox_inches='tight')
plt.show()

