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

        for (int i=0; i<m.nhalfedges(); i++) { // fix the boundary vertices
            if (m.opp(i)!=-1) continue;
            int v = m.from(i);
            nlRowScaling(10.);
            nlBegin(NL_ROW);
            nlCoefficient(v,  1);
            nlRightHandSide(m.point(v)[d]);
            nlEnd(NL_ROW);
        }
        for (int i=0; i<m.nhalfedges(); i++) { // light attachment to the original geometry
            if (m.opp(i)==-1) continue;
            int v1 = m.from(i);
            int v2 = m.to(i);

            nlRowScaling(.2);
            nlBegin(NL_ROW);
            nlCoefficient(v1,  1);
            nlCoefficient(v2, -1);
            nlRightHandSide(m.point(v1)[d] - m.point(v2)[d]);
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

