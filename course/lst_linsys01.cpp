#include <vector>
#include "model.h"

int main(void) {
    Model m("input-face.obj");

    // smooth the surface through Gauss-Seidel iterations
    for (int it=0; it<10000; it++) {
        for (int v=0; v<m.nverts(); v++) {
            if (m.is_boundary_vert(v)) continue; // fix the boundary

            m.point(v) = m.one_ring_barycenter(v);
        }
    }

    std::cout << m;
    return 0;
}
