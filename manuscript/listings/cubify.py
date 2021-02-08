import numpy as np
from mesh import Mesh
from scipy.sparse        import lil_matrix
from scipy.sparse.linalg import lsmr

def normalize(v):
    return v / np.linalg.norm(v)

def cross(v1, v2):
    return [v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0]]

def nearest_axis(n):
    axes = [[1,0,0],[0,1,0],[0,0,1]]
    nmin = -1
    imin = -1
    for i,a in enumerate(axes):
        if np.abs(np.dot(n,a))>nmin:
            nmin = np.abs(np.dot(n,a))
            imin = i
    return imin

m = Mesh("input-face.obj") # load mesh

for dim in range(3): # the problem is separable in x,y,z
    A = lil_matrix((m.ncorners*2, m.nverts))
    b = [m.V[m.dst(c)][dim]-m.V[m.org(c)][dim] for c in range(m.ncorners)] + [0]*m.ncorners
    for c in range(m.ncorners):
        A[c, m.org(c)] = -1 # per-half-edge discretization of the derivative
        A[c, m.dst(c)] =  1

        t = c//3 # triangle id from halfedge id
        n = normalize(cross(m.V[m.T[t][1]]- m.V[m.T[t][0]], m.V[m.T[t][2]]- m.V[m.T[t][0]])) # normal
        if nearest_axis(n)==dim:  # flatten the right dimension of each half-edge
            A[c+m.ncorners, m.org(c)] = -2
            A[c+m.ncorners, m.dst(c)] =  2
    A = A.tocsr() # sparse row matrix for fast matrix-vector multiplication
    x = lsmr(A, b)[0] # call the least squares solver
    for v in range(m.nverts): # apply the computed distortion
        m.V[v][dim] = x[v]

print(m) # output the deformed mesh
