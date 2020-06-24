import numpy as np
import math
import random

def neuron(x, w):
    return 1./(1.+math.exp(-np.dot(x,w)))

u,v,w = [9.538, -1.532, -3.088], [-4.642, -4.089, 5.611], [17.014, 20.803, -26.902]

samples = [[.5,.7,1.],[.1,.5,1.],[.3,.6,1.],[.2,.8,1.],
           [.17,.17,1.],[.2,.3,1.],[.3,.4,1.],[.05,.2,1.],
           [.2,.3,1.],[.8,.3,1.],[.5,.2,1.],[.7,.2,1.],
           [.9,.1,1.],[.8,.4,1.],[.6,.5,1.],[.5,.4,1.]]
labels = [0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.,1.]

samples2 = [[.9, .5, 1.],[.79, .6, 1.],[.73, .7, 1.],[.9, .8, 1.],[.95, .4, 1.]]
labels2 = [0.,0.,0.,0.,0.]

samples = samples + samples2
labels = labels + labels2

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True
plt.rc('font', size=20)

fig,ax = plt.subplots(1, figsize=(6.40*1.25,6.40),dpi=150)


res = 30
x0 = np.arange(0, 1., 1./res)
x1 = np.arange(0, 1., 1./res)

#Y = np.array([[neuron([neuron([a,b,1.], u), neuron([a,b,1],v), 1.], w)/2. for a in x0] for b in x1])
Y = np.array([[np.dot([neuron([a,b,1.], u), neuron([a,b,1],v), 1.], w)/2. for a in x0] for b in x1])
#Y = np.array([[neuron([a,b,1.], u)/2. for a in x0] for b in x1])
#Y = np.array([[neuron([a,b,1.], v)/2. for a in x0] for b in x1])
X0, X1 = np.meshgrid(x0, x1)

'''
for sample, label in zip(samples,labels):
    if (label>.5): continue
    print(sample[0], sample[1], .5)
#    plt.scatter(sample[0], sample[1], color=c, edgecolors='black',s=200,linewidths=2)
'''

for p in zip(X0.flatten(), X1.flatten(), Y.flatten()):
    print("v %3.3f %3.3f %3.3f" % p)

n = len(x0)

for i in range(n-1):
    for j in range(n-1):
        print("f %d %d %d %d" %(i+j*n+1, i+1+j*n+1, i+1+(j+1)*n+1, i+(j+1)*n+1) )
