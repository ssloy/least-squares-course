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
            double scaling = (m.is_boundary_vert(v) ? 10. : 0.29);
            nlRowScaling(scaling); // the boundary is fixed, the interior has a light attachment
            nlBegin(NL_ROW);
            nlCoefficient(v, 1);
            nlRightHandSide(m.point(v)[d]);
            nlEnd(NL_ROW);
        }

        for (int h=0; h<m.nhalfedges(); h++) { // amplify
            int v1 = m.from(h);
            int v2 = m.to(h);

            nlRowScaling(1.);
            nlBegin(NL_ROW);
            nlCoefficient(v1,  1);
            nlCoefficient(v2, -1);

            nlRightHandSide(2.5*(m.point(v1)[d] - m.point(v2)[d]));
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

