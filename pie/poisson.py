import matplotlib.image as mpimg
import scipy.sparse
from scipy.sparse.linalg import spsolve

base = mpimg.imread('baseball.png')
foot = mpimg.imread('football.png')
w,h = len(foot[0]), len(foot)
ox,oy = 100, 60

D = scipy.sparse.lil_matrix((h, h))
D.setdiag(-1, -1)
D.setdiag(4)
D.setdiag(-1, 1)
A = scipy.sparse.block_diag([D] * w).tolil()
A.setdiag(-1,  1*h)
A.setdiag(-1, -1*h)
A = A.tocsc()

for channel in range(3):
    b = A.dot(foot[:,:,channel].flatten())
#   b[0:w]    = base[oy,ox:ox+w,channel]
#   b[0::w]   = base[oy:oy+h, ox, channel]
#   b[-w:]    = base[oy+h,ox:ox+w,channel]
#   b[w-1::w] = base[oy:oy+h, ox+w, channel]

    x = spsolve(A, b)
    x = x.reshape((h, w))
    base[oy:oy+h,ox:ox+h, channel] = x

mpimg.imsave('poisson.png', base)

