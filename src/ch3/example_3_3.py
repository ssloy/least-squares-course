from mesh import Mesh
import scipy.sparse

m = Mesh("input-face.obj") # load mesh

A = scipy.sparse.lil_matrix((m.nverts, m.nverts))
for v in range(m.nverts): # build a smoothing operator as a sparse matrix
    if m.on_border(v):
        A[v,v] = 1 # fix boundary verts
    else:
        neigh_list = m.neighbors(v)
        for neigh in neigh_list:
            A[v, neigh] = 1/len(neigh_list) # 1-ring barycenter for interior
A = A.tocsr() # sparse row matrix for fast matrix-vector multiplication

for _ in range(8192): # smooth the surface through Gauss-Seidel iterations
    m.V = A.dot(m.V)

print(m) # output smoothed mesh
