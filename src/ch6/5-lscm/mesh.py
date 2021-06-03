import numpy as np

def project_triangle(p0, p1, p2):
    X = np.subtract(p1, p0) # construct an orthonormal 3d basis
    X = X/np.linalg.norm(X)
    Z = np.cross(X, np.subtract(p2, p0))
    Z = Z/np.linalg.norm(Z)
    Y = np.cross(Z, X)
    z0 = np.array([0,0]) # project the triangle to the 2d basis (X,Y)
    z1 = np.array([np.linalg.norm(np.subtract(p1, p0)), 0])
    z2 = np.array([np.dot(np.subtract(p2, p0), X), np.dot(np.subtract(p2, p0), Y)])
    return [z1-z0, z2-z1, z0-z2]

class Mesh():
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

    @property
    def nverts(self):
        return len(self.V)

    @property
    def ntriangles(self):
        return len(self.T)

    def __str__(self):
        ret = ""
        for v in self.V:
            ret = ret + ("v %f %f %f\n" % (v[0], v[1], v[2]))
        for t in self.T:
            ret = ret + ("f %d %d %d\n" % (t[0]+1, t[1]+1, t[2]+1))
        return ret
