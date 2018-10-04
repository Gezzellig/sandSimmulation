#ifndef CPP_GRID_H
#define CPP_GRID_H

#include <list>
#include <vector>

#include "point.h"

struct Grid
{
    double lambda_val;
    vector<vector<Point*>> points;
    list<Point*> edge_points;
    list<Spring*> springs;

    Grid(double lambda_val);
    Grid(double lambda_val, vector<vector<Point*>> points, list<Point*> edge_points, list<Spring*> springs);
    ~Grid();
    Grid(const Grid &g2);
    void remove_spring(Spring *spring);
};

Grid create_square_grid(size_t dim, double field_size, double strain_normal, double strain_deviation);

void print_grid(Grid *g);

#endif //CPP_GRID_H
