import matplotlib.pyplot as plt
import numpy as np
import math

samples = [[.5,.7,1.],[.1,.5,1.],[.3,.6,1.],[.2,.8,1.],
           [.17,.17,1.],[.2,.3,1.],[.3,.4,1.],[.05,.2,1.],
           [.2,.3,1.],[.8,.3,1.],[.5,.2,1.],[.7,.2,1.],
           [.9,.1,1.],[.8,.4,1.],[.6,.5,1.],[.5,.4,1.]]
labels = [0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.,1.]

samples += [[.97,.03,1],[.97,.1,1.],[.98,.07,1.],[.96,.04,1.],[.93,.05,1.], [.91, .07, 1.], [.94, .13, 1.], [.95, .17, 1.], [.98, .02, 1.], [.94, .06, 1.], [.93, .08, 1.] , [.95, .11, 1.] , [.96, .04, 1.] , [.99, .02, 1.] , [.97, .09, 1.]]
labels += [1.]*15

n = len(samples)

A = np.matrix(np.zeros((n,3)))
b = np.matrix(np.zeros((n,1)))
for i in range(n):
    A[i,0] = samples[i][0]
    A[i,1] = samples[i][1]
    A[i,2] = samples[i][2]
    b[i,0] = labels[i]


X = np.linalg.inv(A.transpose()*A)*A.transpose()*b
X = X.transpose().tolist()[0]

fig,ax = plt.subplots(1, figsize=(6.40,6.40),dpi=100)

res = 100
x0 = np.arange(0, 1., 1./res)
x1 = np.arange(0, 1., 1./res)

Y = [[np.dot([a, b, 1.], X)  for a in x0] for b in x1]

X0, X1 = np.meshgrid(x0, x1)
plt.contourf(X0, X1, Y, 100, cmap=plt.cm.RdYlGn)
plt.colorbar()
plt.contour(X0, X1, Y,levels=[.49995, .50005], colors='k', linestyles='--')


for sample, label in zip(samples,labels):
    c = 'g'
    if (label<.5): c = 'r'
    plt.scatter(sample[0], sample[1], color=c, edgecolors='black')

plt.tight_layout()
#plt.gca().axes.get_yaxis().set_visible(False)
#plt.gca().axes.get_xaxis().set_visible(False)
plt.show()

