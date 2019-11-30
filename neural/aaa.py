import matplotlib.pyplot as plt
import numpy as np
import math

def neuron(x, w):
    return 1./(1.+math.exp(-np.dot(x,w)))

weights = [.0, .0, .0]

samples = [[.5, .7, 1.], [.1, .5, 1.], [.3, .6, 0.], [.2, .8, 0.], [.17, .17, 1.], [.2, .3, 1.], [.3, .4, 1.], [.05, .2, 1.], [.2, .3, 1.], [.8, .3, 1.], [.5, .2, 1.], [.7, .2, 1.], [.9, 0., 1.], [.8, .4, 1.], [.6, .5, 1.], [.5, .4, 1.]]
labels = [0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.,1.]

samples2 = [[.9, .5, 1.],[.79, .6, 1.],[.73, .7, 1.],[.9, .8, 1.],[.95, .4, 1.]]
labels2 = [0.,0.,0.,0.,0.]

samples = samples + samples2
labels = labels + labels2

for iter in range(0,1000):
#    E = 0
#    for sample, label in zip(samples,labels):
#        E += (label - neuron(sample,weights))**2
#    print("E =",E)
    for sample, label in zip(samples,labels):
        for i in range(3):
            out = neuron(sample, weights)
            weights[i] += 0.5*(label-out)*out*(1.-out)*sample[i]

print(weights)



res = 100
x0 = np.arange(0, 1., 1./res)
x1 = np.arange(0, 1., 1./res)

Y = [[neuron([a,b,1.], weights) for a in x0] for b in x1]

X0, X1 = np.meshgrid(x0, x1)
plt.contourf(X0, X1, Y,100, cmap=plt.cm.RdYlGn)
plt.colorbar()

for sample, label in zip(samples,labels):
    c = 'g'
    if (label<.5): c = 'r'
    plt.scatter(sample[0], sample[1], color=c, edgecolors='black')



plt.show()

