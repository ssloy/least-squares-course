import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import math
import random

def neuron(x, w):
    return 1./(1.+math.exp(-np.dot(x,w)))

#u = [random.random(), random.random(), random.random()]
#v = [random.random(), random.random(), random.random()]
#w = [random.random(), random.random(), random.random()]
u = [0.814, 0.779, 0.103] # small random values
v = [0.562, 0.310, 0.591]
w = [0.884, 0.934, 0.649]

samples = [[.5, .7, 1.], [.1, .5, 1.], [.3, .6, 0.], [.2, .8, 0.], [.17, .17, 1.], [.2, .3, 1.], [.3, .4, 1.], [.05, .2, 1.], [.2, .3, 1.], [.8, .3, 1.], [.5, .2, 1.], [.7, .2, 1.], [.9, .1, 1.], [.8, .4, 1.], [.6, .5, 1.], [.5, .4, 1.]]
labels = [0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.,1.]

samples2 = [[.9, .5, 1.],[.79, .6, 1.],[.73, .7, 1.],[.9, .8, 1.],[.95, .4, 1.]]
labels2 = [0.,0.,0.,0.,0.]

samples = samples + samples2
labels = labels + labels2

alpha = 1.0 # learning rate


fig,ax = plt.subplots(1, figsize=(6.40,6.40),dpi=100)

res = 100
x0 = np.arange(0, 1., 1./res)
x1 = np.arange(0, 1., 1./res)


def draw(i):
    for iter in range(0,30):
        for x, label in zip(samples,labels):
            for i in range(3):
                xprime = [neuron(x, u), neuron(x, v), 1.]
                out_w = neuron(xprime, w)
                w[i] += alpha*(label-out_w)*out_w*(1.-out_w)*xprime[i]
    
                out_u = neuron(x, u)
                u[i] += alpha*(label-out_w)*out_w*(1.-out_w)*out_u*(1.-out_u)*x[i]

                out_v = neuron(x, v)
                v[i] += alpha*(label-out_w)*out_w*(1.-out_w)*out_v*(1.-out_v)*x[i]

    Y = [[neuron([neuron([a,b,1.], u), neuron([a,b,1],v), 1.], w) for a in x0] for b in x1]
    X0, X1 = np.meshgrid(x0, x1)
    plt.contourf(X0, X1, Y, 100, vmin=0., vmax=1., cmap=plt.cm.RdYlGn)
#    plt.colorbar()

    for sample, label in zip(samples,labels):
        c = 'g'
        if (label<.5): c = 'r'
        plt.scatter(sample[0], sample[1], color=c, edgecolors='black')

    E = 0
    for x, label in zip(samples,labels):
        xprime = [neuron(x, u), neuron(x, v), 1.]
        E += (label - neuron(xprime,w))**2
    print("E =",E)
    ax.text(0.05, 0.05, ("Error: %3.3f" % E) , transform=ax.transAxes, fontsize=24)

def animate(i):
    ax.clear()
    draw(i)
    return ax,

draw(0)
plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)


ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 100), interval=1, blit=False, save_count=100)
ani.save('classifier.gif', dpi=80, writer='imagemagick')

#from matplotlib.animation import FFMpegWriter
#writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#ani.save("classifier.mp4", writer=writer)

#plt.show()

