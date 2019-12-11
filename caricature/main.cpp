#include <vector>
#include <iostream>

#include "OpenNL_psm.h"
#include "geometry.h"
#include "model.h"

int main(int argc, char** argv) {
    if (argc<2) {
        std::cerr << "Usage: " << argv[0] << " obj/model.obj" << std::endl;
        return 1;
    }

    Model m(argv[1]);

    for (int d=0; d<3; d++) { // solve for x, y and z separately
        nlNewContext();
        nlSolverParameteri(NL_NB_VARIABLES, m.nverts());
        nlSolverParameteri(NL_LEAST_SQUARES, NL_TRUE);
        nlBegin(NL_SYSTEM);
        nlBegin(NL_MATRIX);

        for (int v=0; v<m.nverts(); v++) { // attachment to the original geometry
            double scaling = (m.is_boundary_vert(v) ? 10. : 0.03);
            nlRowScaling(scaling); // the boundary is fixed, the interior has a light attachment
            nlBegin(NL_ROW);
            nlCoefficient(v, 1);
            nlRightHandSide(m.point(v)[d]);
            nlEnd(NL_ROW);
        }

        for (int v=0; v<m.nverts(); v++) { // amplify the curvature
            nlRowScaling(1.);
            nlBegin(NL_ROW);
            int nneigh = m.incident_halfedges(v).size();
            nlCoefficient(v,  nneigh);
            Vec3f curvature = m.point(v)*nneigh;
            for (int hid : m.incident_halfedges(v)) {
                nlCoefficient(m.to(hid),  -1);
                curvature = curvature - m.point(m.to(hid));
            }
            nlRightHandSide(2.5*curvature[d]);
            nlEnd(NL_ROW);
        }

        nlEnd(NL_MATRIX);
        nlEnd(NL_SYSTEM);
        nlSolve();

        for (int i=0; i<m.nverts(); i++) {
            m.point(i)[d] = nlGetVariable(i);
        }
    }

    std::cout << m;
    return 0;
}

