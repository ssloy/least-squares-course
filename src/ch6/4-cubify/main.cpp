#include "OpenNL_psm.h"
#include "model.h"

const vec3 axes[] = {vec3(1,0,0), vec3(-1,0,0), vec3(0,1,0), vec3(0,-1,0), vec3(0,0,1), vec3(0,0,-1)};
int snap(vec3 n) { // returns 0,1 or 2: the coordinate axis closest to the given normal
    double nmin = -2.0;
    int    imin = -1;
    for (int i=0; i<6; i++) {
        double t = n*axes[i];
        if (t>nmin) {
            nmin = t;
            imin = i;
        }
    }
    return imin/2;
}

int main() {
    Model m("../input-face.obj");

    // for each facet find the coordinate axis (x,y or z) closest to the normal
    std::vector<int> nearest_axis(m.nfaces());
    for (int i=0; i<m.nfaces(); i++) {
        vec3 v[3];
        for (int j=0; j<3; j++) v[j] = m.point(m.vert(i, j));
        vec3 n = cross(v[1]-v[0], v[2]-v[0]).normalize();
        nearest_axis[i] = snap(n);
    }

    for (int d=0; d<3; d++) { // solve for x, y and z separately
        nlNewContext();
        nlSolverParameteri(NL_NB_VARIABLES, m.nverts());
        nlSolverParameteri(NL_LEAST_SQUARES, NL_TRUE);
        nlBegin(NL_SYSTEM);
        nlBegin(NL_MATRIX);

        for (int h=0; h<m.nhalfedges(); h++) {
            int v1 = m.from(h);
            int v2 = m.to(h);

            nlRowScaling(1.); // light attachment to the old geometry
            nlBegin(NL_ROW);
            nlCoefficient(v1,  1);
            nlCoefficient(v2, -1);
            nlRightHandSide(m.point(v1)[d] - m.point(v2)[d]);
            nlEnd(NL_ROW);

            int face = h/3;
            int axis = nearest_axis[face];
            if (d!=axis) continue;

            nlRowScaling(2.); // flatten
            nlBegin(NL_ROW);
            nlCoefficient(v1,  1);
            nlCoefficient(v2, -1);
            nlEnd(NL_ROW);
        }

        nlEnd(NL_MATRIX);
        nlEnd(NL_SYSTEM);
        nlSolve();

        for (int i=0; i<m.nverts(); i++)
            m.point(i)[d] = nlGetVariable(i);
    }

    std::cout << m;
    return 0;
}

