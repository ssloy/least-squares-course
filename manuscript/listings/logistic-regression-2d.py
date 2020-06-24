import numpy as np
import math

def p(x, w):
    return 1./(1.+math.exp(-np.dot(x,w)))

samples = [[.5,.7,1.],[.1,.5,1.],[.3,.6,1.],[.2,.8,1.],
           [.17,.17,1.],[.2,.3,1.],[.3,.4,1.],[.05,.2,1.],
           [.2,.3,1.],[.8,.3,1.],[.5,.2,1.],[.7,.2,1.],
           [.9,.1,1.],[.8,.4,1.],[.6,.5,1.],[.5,.4,1.]]
labels = [0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.,1.]

n = len(samples)
X = np.matrix(samples)
y = np.matrix(labels).T
wk = np.matrix([[.3], [.7], [-.02]]) # small random numbers

l = 0.001 # regularization coefficient
for _ in range(5):
    pk = np.matrix([p(xi,wk) for xi in samples]).T
    Vk = np.matrix(np.diag([pk[i,0]*(1.-pk[i,0]) for i in range(n)]))
    wk += np.linalg.inv(X.T*Vk*X + l*np.matrix(np.identity(len(samples[0]))))*(X.T*(y-pk) - l*wk)
print(wk)
