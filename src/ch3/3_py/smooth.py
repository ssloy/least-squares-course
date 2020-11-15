from mesh import Mesh

m = Mesh("../input-face.obj")

for _ in range(512):
    for v in range(m.nverts()):
        if m.on_border(v): continue
        bary = m.one_ring_barycenter(v)

#print(m)
