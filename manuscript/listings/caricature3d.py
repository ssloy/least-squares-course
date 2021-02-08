from mesh import Mesh
from scipy.sparse.linalg import lsmr
from scipy.sparse import lil_matrix

m = Mesh("input-face.obj") # load mesh

A = lil_matrix((m.nverts+m.ncorners, m.nverts))
for v in range(m.nverts): # per-vertex attachment to the original geometry
    if m.on_border(v):    # hard on the boundary
        A[v,v] = 10
    else:                 # light on the interior
        A[v,v] = .29
for c in range(m.ncorners): # per-half-edge discretization of the derivative
    A[m.nverts+c, m.org(c)] = -1
    A[m.nverts+c, m.dst(c)] =  1
A = A.tocsr() # sparse row matrix for fast matrix-vector multiplication

for dim in range(3): # the problem is separable in x,y,z; the matrix A is the same, the right hand side changes
    b = [m.V[v][dim]*10 if m.on_border(v) else m.V[v][dim]*.29 for v in range(m.nverts)] + \
        [2.5*(m.V[m.dst(c)][dim]-m.V[m.org(c)][dim]) for c in range(m.ncorners)]
    x = lsmr(A, b)[0] # call the least squares solver
    for v in range(m.nverts): # apply the computed distortion
        m.V[v][dim] = x[v]

print(m) # output the deformed mesh

