from mesh import Mesh
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import lsmr
from scipy.linalg import svd
m = Mesh("diablo.obj")
eij = [np.matrix(m.V[m.dst(c)] - m.V[m.org(c)]).T for c in range(m.ncorners)] # reference geometry for each half-edge
lock = [1175, 1765, 381, 2383, 1778] # id of the vertices to constrain
disp = [[0,0,-0.5], [0,0,0.5], [0,0,-0.5], [0,0,0.5], [1.5,0,0]] # displacement for the constrained vertices
for v,d in zip(lock, disp): # apply the displacement
    m.V[v] = m.V[v] + d
A = lil_matrix((m.ncorners+len(lock), m.nverts))
for c in range(m.ncorners): # Least-squares verion of Poisson's problem
    A[c, m.dst(c)], A[c, m.org(c)] =  1, -1
for i,v in enumerate(lock):  # the vertices are locked
    A[m.ncorners+i, v] = 100 # via quadratic penalty
A = A.tocsr() # convert to compressed sparse row format for faster matrix-vector muliplications
for _ in range(100):
    R = [] # rotation per vertex
    for v in range(m.nverts): # solve for rotations
        M = np.zeros(3)
        c = m.v2c[v] # half-edge departing from v
        while True: # iterate through all half-edges departing from v
            M = M + np.matrix(m.V[m.dst(c)] - m.V[m.org(c)]).T*eij[c].T
            c = m.c2c[c] # next around vertex
            if c==m.v2c[v]: break
        U, s, VT = svd(M)
        R.append(np.dot(U,VT)) # rotation matrix for the neighborhood of vertex v
    for dim in range(3): # the problem is separable in x,y,z
        b = [(R[m.org(c)]*eij[c])[dim,0] for c in range(m.ncorners)] + [100*m.V[v][dim] for v,d in zip(lock, disp)]
        x = lsmr(A, b)[0] # call the least squares solver
        for v in range(m.nverts): # apply the computed deformation
            m.V[v][dim] = x[v]
print(m) # output the deformed mesh
