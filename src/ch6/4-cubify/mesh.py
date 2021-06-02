import numpy as np

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

    @property
    def ncorners(self):
        return self.ntriangles*3;

    def normal(self, t):
        n = np.cross(self.V[self.T[t][1]]-self.V[self.T[t][0]], self.V[self.T[t][2]]-self.V[self.T[t][0]])
        return n / np.linalg.norm(n)

    def org(self, c):
        return self.T[c//3][c%3]

    def dst(self, c):
        return self.T[c//3][(c+1)%3]

    def __str__(self):
        ret = ""
        for v in self.V:
            ret = ret + ("v %f %f %f\n" % (v[0], v[1], v[2]))
        for t in self.T:
            ret = ret + ("f %d %d %d\n" % (t[0]+1, t[1]+1, t[2]+1))
        return ret
