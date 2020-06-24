#ifndef __MODEL_H__
#define __MODEL_H__
#include <vector>
#include <string>
#include "geometry.h"

class Model {
private:
    std::vector<vec3> verts;
    std::vector<vec3i> faces;
    std::vector<std::vector<int> > v2h; // vertex to halfedge incidency
    std::vector<int> opposites; // halfedges
    void compute_opposites();
public:
    Model(const char *filename);

    int nverts();
    int nfaces();
    int nhalfedges();

    vec3 &point(int i);
    int vert(int fi, int li);
    void get_bbox(vec3 &min, vec3 &max);
    void print_obj();

    bool is_boundary_vert(int v);

    int from(int hid);
    int to(int hid);
    int opp(int hid);
    std::vector<int> &incident_halfedges(int v);
};

std::ostream& operator<<(std::ostream& out, Model &m);

#endif //__MODEL_H__

