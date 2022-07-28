import matplotlib.image as mpimg
import scipy.sparse
from scipy.sparse.linalg import lsmr

base = mpimg.imread('baseball.png')
foot = mpimg.imread('football.png')
w,h = len(foot[0]), len(foot)
ox,oy = 100, 60 # glue the football here

A = scipy.sparse.lil_matrix((2*w+2*h + 2*(w-1)*(h-1), w*h))
for i in range(0,w):
    A[  i, i        ] = 1 #    top data fitting
    A[w+i, i+(h-1)*w] = 1 # bottom data fitting
for j in range(0,h):
    A[2*w  +j,     j*w] = 1 #  left data fitting
    A[2*w+h+j, w-1+j*w] = 1 # right data fitting
cnt = 2*w+2*h
for j in range(0,h-1): # gradient matrix
    for i in range(0,w-1):
        A[cnt,   i   + j*w] = -1
        A[cnt,   i+1 + j*w] =  1
        A[cnt+1, i +  j   *w] = -1
        A[cnt+1, i + (j+1)*w] =  1
        cnt += 2
A = A.tocsc() # sparse row matrix for fast matrix-vector multiplication

for channel in range(3):
    b = A.dot(foot[:,:,channel].flatten()) # fill the gradient part of the r.h.s.
    b[0:w]    = base[oy,ox:ox+w,channel]   # top data fitting
    b[w:2*w]  = base[oy+h,ox:ox+w,channel] # bottom data fitting
    b[2*w  :2*w+h]   = base[oy:oy+h, ox, channel]   # left data fitting
    b[2*w+h:2*w+2*h] = base[oy:oy+h, ox+w, channel] # right data fitting

    x = lsmr(A, b)[0] # call the least squares solver
    x[x > 1] = 1
    x[x < 0] = 0
    base[oy:oy+h,ox:ox+w, channel] = x.reshape((h, w)) # glue the football
mpimg.imsave('result.png', base)
