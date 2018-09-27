#ifndef CPP_GRID_H
#define CPP_GRID_H

#include "point.h"

struct Grid
{
    double lambda_val;
    list<Point> points;
    list<Point> edge_points;
    list<Spring*> springs;

    Grid(double lambda_val, list<Point> points, list<Point> edge_points, list<Spring*> springs);
    void remove_spring(Spring *spring);
};
#endif //CPP_GRID_H
