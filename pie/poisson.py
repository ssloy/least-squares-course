# https://en.wikipedia.org/wiki/Discrete_Poisson_equation
# https://github.com/PPPW/poisson-image-editing/blob/master/poisson_image_editing.py
# https://github.com/willemmanuel/poisson-image-editing/blob/bd46bed95cbfc5e2d884349282eae40a085b5d54/poisson.py#L90
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.sparse
from scipy.sparse.linalg import spsolve


base = mpimg.imread('baseball.png')
foot = mpimg.imread('debug.png')
w,h = len(foot[0]), len(foot)
ox,oy = 105, 58

A = scipy.sparse.lil_matrix((w*h, w*h))
A.setdiag(-1, -1)
A.setdiag(4)
A.setdiag(-1, 1)
A.setdiag(-1,  1*w)
A.setdiag(-1, -1*w)


L = A.tocsc()

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

for channel in range(3):
    foot[:,:, channel] = 1
#    print(foot[:,:, channel])
    b = L.dot(foot[:,:,channel].flatten())
    b = L.dot([1]*(w*h))
    print(b)
    print(L.toarray())
    b[w*10:w*11] -= base[10,ox:ox+w,channel]
#    print(base[10,ox:ox+w,channel])


    x = spsolve(L, b)
    x = x.reshape((h, w))
#    print(x)
#    x[x > 1] = 1
#    x[x < 0] = 0

    base[oy:oy+h,ox:ox+h, channel] = x
    break

plt.imshow(base)
plt.show()

