#include <vector>
#include "model.h"

int main(void) {
    Model m("input-face.obj");

    // for each vertex compute the Gaussian curvature
    std::vector<vec3> curv(m.nverts(), vec3(0,0,0));
    for (int v=0; v<m.nverts(); v++) {
        curv[v] = m.curvature(v);
    }

    // smooth the surface through Gauss-Seidel iterations
    for (int it=0; it<100; it++) {
        for (int v=0; v<m.nverts(); v++) {
            if (m.is_boundary_vert(v)) continue; // fix the boundary

            m.point(v) = m.one_ring_barycenter(v) + curv[v]*2.1;
        }
    }

    std::cout << m;
    return 0;
}
