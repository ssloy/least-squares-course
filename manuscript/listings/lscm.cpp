#include "OpenNL_psm.h"
#include "model.h"

void project_triangle(const vec3& p0, const vec3& p1, const vec3& p2, vec2& z0, vec2& z1, vec2& z2) {
    vec3 X = (p1 - p0).normalize(); // construct an orthonormal 3d basis
    vec3 Z = cross(X, p2 - p0).normalize();
    vec3 Y = cross(Z, X);
    z0 = vec2(0,0); // project the triangle to the 2d basis (X,Y)
    z1 = vec2((p1 - p0).norm(), 0);
    z2 = vec2((p2 - p0)*X, (p2 - p0)*Y);
}

int main() {
    Model m("../input.obj");

    nlNewContext();
    nlSolverParameteri(NL_NB_VARIABLES, 2*m.nverts()); // u0,v0,u1,v1, ...
    nlSolverParameteri(NL_LEAST_SQUARES, NL_TRUE);
    nlBegin(NL_SYSTEM);

    // select two arbitrary vertices to pin
    int lock1 = 10324 % m.nverts(), lock2 = 35492 % m.nverts();
    nlSetVariable(lock1*2+0, 0); // first vertex is pinned to (0,0)
    nlSetVariable(lock1*2+1, 0);
    nlSetVariable(lock2*2+0, 1); // the second one to (1,1)
    nlSetVariable(lock2*2+1, 1);
    nlLockVariable(lock1*2+0); // eliminate 4 constrained variables from the system
    nlLockVariable(lock1*2+1);
    nlLockVariable(lock2*2+0);
    nlLockVariable(lock2*2+1);

    nlBegin(NL_MATRIX);
    for (int f=0; f<m.nfaces(); f++) { // for each triangle ijk
        int i=m.vert(f, 0), j=m.vert(f, 1), k=m.vert(f, 2);
        vec3 pi=m.point(i), pj=m.point(j), pk=m.point(k);

        vec2 zi, zj, zk; // project the triangle to a local 2d basis
        project_triangle(pi, pj, pk, zi, zj, zk);
        vec2 ejk = zk-zj, eki = zi-zk, eij = zj-zi;

        nlBegin(NL_ROW); // (grad u)[0] = (grad v)[1]
        nlCoefficient(i*2,   ejk.x);
        nlCoefficient(j*2,   eki.x);
        nlCoefficient(k*2,   eij.x);
        nlCoefficient(i*2+1, ejk.y);
        nlCoefficient(j*2+1, eki.y);
        nlCoefficient(k*2+1, eij.y);
        nlEnd(NL_ROW);

        nlBegin(NL_ROW); // (grad u)[1] = -(grad v)[0]
        nlCoefficient(i*2,    ejk.y);
        nlCoefficient(j*2,    eki.y);
        nlCoefficient(k*2,    eij.y);
        nlCoefficient(i*2+1, -ejk.x);
        nlCoefficient(j*2+1, -eki.x);
        nlCoefficient(k*2+1, -eij.x);
        nlEnd(NL_ROW);
    }
    nlEnd(NL_MATRIX);
    nlEnd(NL_SYSTEM);
    nlSolve();

    for (int i=0; i<m.nverts(); i++) { // apply the computed flattening
        m.point(i).x = nlGetVariable(i*2);
        m.point(i).y = nlGetVariable(i*2+1);
        m.point(i).z = 0;
    }
    std::cout << m;
    return 0;
}

