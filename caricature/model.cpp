#include <iostream>
#include <cassert>
#include <fstream>
#include <sstream>
#include "model.h"

// fills verts and faces arrays, supposes .obj file to have "f " entries without slashes
Model::Model(const char *filename) : verts(), faces(), v2h(), opposites() {
    std::ifstream in;
    in.open (filename, std::ifstream::in);
    if (in.fail()) {
        std::cerr << "Failed to open " << filename << std::endl;
        return;
    }
    std::string line;
    while (!in.eof()) {
        std::getline(in, line);
        std::istringstream iss(line.c_str());
        char trash;
        if (!line.compare(0, 2, "v ")) {
            iss >> trash;
            Vec3f v;
            for (int i=0;i<3;i++) iss >> v[i];
            verts.push_back(v);
        } else if (!line.compare(0, 2, "f ")) {
            Vec3i f;
            int idx, cnt=0;
            iss >> trash;
            while (iss >> idx) {
                idx--; // in wavefront obj all indices start at 1, not zero
                f[cnt++] = idx;
            }
            if (3==cnt) faces.push_back(f);
        }
    }
    std::cerr << "# v# " << verts.size() << " f# "  << faces.size() << std::endl;

    v2h = std::vector<std::vector<int> >(verts.size());
    for (int i=0; i<nfaces(); i++) {
        for (int k=0; k<3; k++) {
            v2h[vert(i,k)].push_back(i*3+k);
        }
    }
    opposites = std::vector<int>(nfaces()*3, -1);
    compute_opposites();
}

bool Model::is_boundary_vert(int v) {
    for (int hid : incident_halfedges(v)) {
        if (opp(hid)<0) return true;
    }
    return false;
}

int Model::from(int hid) {
    return vert(hid/3, hid%3);
}

int Model::to(int hid) {
    return vert(hid/3, (hid+1)%3);
}

int Model::opp(int hid) {
    return opposites[hid];
}

void Model::compute_opposites() {
    for (int h1=0; h1<nfaces()*3; h1++) {
        int v1 = from(h1);
        int v2 = to(h1);

        for (int j=0; j<(int)v2h[v2].size(); j++) {
            int h2 = v2h[v2][j];
            assert(v2==from(h2));
            int v3 = to(h2);
            if (v3==v1) {
                opposites[h1] = h2;
                opposites[h2] = h1;
            }
        }
    }
}

int Model::nverts() {
    return (int)verts.size();
}

int Model::nfaces() {
    return (int)faces.size();
}

int Model::nhalfedges() {
    return faces.size()*3;
}
std::vector<int> &Model::incident_halfedges(int v) {
    return v2h[v];
}

void Model::get_bbox(Vec3f &min, Vec3f &max) {
    min = max = verts[0];
    for (int i=1; i<(int)verts.size(); ++i) {
        for (int j=0; j<3; j++) {
            min[j] = std::min(min[j], verts[i][j]);
            max[j] = std::max(max[j], verts[i][j]);
        }
    }
    std::cerr << "bbox: [" << min << " : " << max << "]" << std::endl;
}

Vec3f &Model::point(int i) {
    assert(i>=0 && i<nverts());
    return verts[i];
}

int Model::vert(int fi, int li) {
    assert(fi>=0 && fi<nfaces() && li>=0 && li<3);
    return faces[fi][li];
}

std::ostream& operator<<(std::ostream& out, Model &m) {
    for (int i=0; i<m.nverts(); i++) {
        out << "v " << m.point(i) << std::endl;
    }
    for (int i=0; i<m.nfaces(); i++) {
        out << "f ";
        for (int k=0; k<3; k++) {
            out << (m.vert(i,k)+1) << " ";
        }
        out << std::endl;
    }
    return out;
}

