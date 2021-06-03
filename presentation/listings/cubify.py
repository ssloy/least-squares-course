import numpy as np
from mesh import Mesh
from scipy.sparse        import lil_matrix
from scipy.sparse.linalg import lsmr

m = Mesh("input-face.obj") # load mesh

def nearest_axis(n):
    return np.argmax([np.abs(np.dot(n, a)) for a in [[1,0,0],[0,1,0],[0,0,1]]])
for dim in range(3): # the problem is separable in x,y,z
    A = lil_matrix((m.ncorners*2, m.nverts))
    b = [m.V[m.dst(c)][dim]-m.V[m.org(c)][dim] for c in range(m.ncorners)]+[0]*m.ncorners
    for c in range(m.ncorners):
        A[c, m.org(c)] = -1 # per-half-edge discretization of the derivative
        A[c, m.dst(c)] =  1

        t = c//3 # triangle id from halfedge id
        if nearest_axis(m.normal(t))==dim:  # flatten the right dimension
            A[c+m.ncorners, m.org(c)] = -2
            A[c+m.ncorners, m.dst(c)] =  2
    A = A.tocsr() # sparse row matrix for fast matrix-vector multiplication
    x = lsmr(A, b)[0] # call the least squares solver
    for v in range(m.nverts): # apply the computed distortion
        m.V[v][dim] = x[v]
print(m) # output the deformed mesh
