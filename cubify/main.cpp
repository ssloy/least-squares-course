#include <vector>
#include <iostream>

#include "OpenNL_psm.h"
#include "geometry.h"
#include "model.h"

const Vec3f axes[] = {Vec3f(1,0,0), Vec3f(-1,0,0), Vec3f(0,1,0), Vec3f(0,-1,0), Vec3f(0,0,1), Vec3f(0,0,-1)};
int snap(Vec3f n) { // returns the coordinate axis closest to the given normal
    double nmin = -2.0;
    int    imin = -1;
    for (int i=0; i<6; i++) {
        double t = n*axes[i];
        if (t>nmin) {
            nmin = t;
            imin = i;
        }
    }
    return imin;
}

int main(int argc, char** argv) {
    if (argc<2) {
        std::cerr << "Usage: " << argv[0] << " obj/model.obj" << std::endl;
        return 1;
    }

    Model m(argv[1]);

    std::vector<int> nearest_axis(m.nfaces());
    for (int i=0; i<m.nfaces(); i++) {
        Vec3f v[3];
        for (int j=0; j<3; j++) v[j] = m.point(m.vert(i, j));
        Vec3f n = cross(v[1]-v[0], v[2]-v[0]).normalize();
        nearest_axis[i] = snap(n);
    }

    for (int d=0; d<3; d++) { // solve for x, y and z separately
        nlNewContext();
        nlSolverParameteri(NL_NB_VARIABLES, m.nverts());
        nlSolverParameteri(NL_LEAST_SQUARES, NL_TRUE);
        nlBegin(NL_SYSTEM);
        nlBegin(NL_MATRIX);

        for (int i=0; i<m.nhalfedges(); i++) {
            int v1 = m.from(i);
            int v2 = m.to(i);

            nlRowScaling(1.);
            nlBegin(NL_ROW);
            nlCoefficient(v1,  1);
            nlCoefficient(v2, -1);
            nlRightHandSide(m.point(v1)[d] - m.point(v2)[d]);
            nlEnd(NL_ROW);

            int axis = nearest_axis[i/3]/2;
            if (d!=axis) continue;

            nlRowScaling(2.);
            nlBegin(NL_ROW);
            nlCoefficient(v1,  1);
            nlCoefficient(v2, -1);
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

