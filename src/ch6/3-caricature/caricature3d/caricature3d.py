import scipy.sparse
import numpy as np
from scipy.sparse.linalg import lsmr

class Mesh:
    def __init__(self, filename):
        # parse the .obj file
        V, T = [], []
        with open(filename) as f:
           for line in f.readlines():
               if line.startswith('#'): continue
               values = line.split()
               if not values: continue
               if values[0] == 'v':
                   V.append([float(x) for x in values[1:4]])
               elif values[0] == 'f':
                   T.append([int(x) for x in values[1:4]])
        self.V, self.T = np.array(V), np.array(T)-1

        # compute the adjacency
        self.v2c = np.array([-1]*self.nverts())
        self.c2c = np.array([-1]*self.ntriangles()*3)
        for c in range(self.ntriangles()*3):
            v = self.T[c//3][c%3]
            self.v2c[v] = c
        for c in range(self.ntriangles()*3):
            v = self.T[c//3][c%3]
            self.c2c[c] = self.v2c[v]
            self.v2c[v] = c

    def nverts(self):
        return len(self.V)

    def ntriangles(self):
        return len(self.T)

    def org(self, c):
        return self.T[c//3][c%3]

    def dst(self, c):
        return self.T[c//3][(c+1)%3]

    def prev(self, c):
        return (c//3)*3 + (c+2)%3

    def opposite(self, c):
        cir = c
        result = -1
        while True:
            candidate = m.prev(cir)
            if (self.org(candidate)==self.dst(c) and self.dst(candidate)==self.org(c)):
                result = candidate # we suppose manifold input
            cir = self.c2c[cir]
            if (cir==c): break
        return result

    def on_border(self, v):
        cir = self.v2c[v]
        if cir<0: return False
        while (True):
            if self.opposite(cir)<0: return True
            cir = self.c2c[cir]
            if (cir==self.v2c[v]): break
        return False

m = Mesh("input-face.obj")

for v in range(m.nverts()):
    if m.on_border(v):
        print(m.V[v])

