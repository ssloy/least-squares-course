from mesh import Mesh
import numpy as np
import scipy.sparse
from scipy.sparse.linalg import lsmr

def normalize(v):
    return v / np.linalg.norm(v)

def project_triangle(p0, p1, p2):
    X = normalize(np.subtract(p1, p0)) # construct an orthonormal 3d basis
    Z = normalize(np.cross(X, np.subtract(p2, p0)))
    Y = np.cross(Z, X)
    z0 = np.array([0,0]) # project the triangle to the 2d basis (X,Y)
    z1 = np.array([np.linalg.norm(np.subtract(p1, p0)), 0])
    z2 = np.array([np.dot(np.subtract(p2, p0), X), np.dot(np.subtract(p2, p0), Y)])
    return [z0, z1, z2]

m = Mesh("input-face.obj") # load mesh

# build the system                                          # 2 eq per triangle + 4 eq for pinning verts
A = scipy.sparse.lil_matrix((2*m.ntriangles+4, 2*m.nverts)) # the variables are packed as u0,v0,u1,v1, ...
lock1, lock2 = 10324%m.nverts, 35492%m.nverts  # select two arbitrary vertices to pin
for (t,[i,j,k]) in enumerate(m.T): # for each triangle ijk
    zi,zj,zk = project_triangle(m.V[i], m.V[j], m.V[k]) # project the triangle to a local 2d basis
    ejk = zk-zj # edges of the projected triangle:
    eki = zi-zk # the gradients are computed
    eij = zj-zi # as a function of the edges
    A[t*2+0, i*2  ] =  ejk[0] # (grad u)[0] = (grad v)[1]
    A[t*2+0, j*2  ] =  eki[0]
    A[t*2+0, k*2  ] =  eij[0]
    A[t*2+0, i*2+1] =  ejk[1]
    A[t*2+0, j*2+1] =  eki[1]
    A[t*2+0, k*2+1] =  eij[1]

    A[t*2+1, i*2  ] =  ejk[1] # (grad u)[1] = -(grad v)[0]
    A[t*2+1, j*2  ] =  eki[1]
    A[t*2+1, k*2  ] =  eij[1]
    A[t*2+1, i*2+1] = -ejk[0]
    A[t*2+1, j*2+1] = -eki[0]
    A[t*2+1, k*2+1] = -eij[0]
A[-1,lock2*2+1] = A[-2,lock2*2+0] = A[-3,lock1*2+1] = A[-4,lock1*2+0] = 10 # quadratic penalty

A = A.tocsr() # convert to compressed sparse row format for faster matrix-vector muliplications
b = [0]*(2*m.ntriangles) + [0,0,10,10] # one pinned to (0,0), another to (1,1)
x = lsmr(A, b)[0] # call the least squares solver

for v in range(m.nverts): # apply the computed flattening
    m.V[v] = np.array([x[v*2], x[v*2+1], 0])
print(m) # output the deformed mesh
