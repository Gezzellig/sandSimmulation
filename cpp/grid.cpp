
#include <list>
#include <iostream>
#include <random>
#include "grid.h"
#include "spring.h"

using namespace std;

Grid::Grid(double lambda_val)
    : lambda_val(lambda_val)
{

}

Grid::Grid(double lambda_val, vector<Point*> points, list<Point*> edge_points, list<Spring*> springs)
    : lambda_val(lambda_val), points(points), edge_points(edge_points), springs(springs)
{

}

Grid::~Grid()
{
    for (auto p : points) {
        delete p;
    }
    for (auto spring: springs)
        delete spring;
}

//Grid::Grid(const Grid &g2)
//{
//    cout << "copy constructor of grid called; this will fail as it's not implemented yet" << endl;
//}

void Grid::remove_spring(Spring *spring)
{
    springs.remove(spring);
}

Position calc_square_position(size_t w, size_t h, size_t dim, double field_size)
{
    // TODO: random small offsets from uniform dist
    double xpos = field_size / (dim-1) * (dim - (h+1));
    double ypos = field_size / (dim-1) * w;
    return make_pair(xpos, ypos);
}

Grid *create_square_grid(size_t dim, double field_size, double strain_normal, double strain_deviation)
{
    double start_lambda = field_size / (dim - 1);

//    double springconstant = 1.0;

    default_random_engine gen;
    normal_distribution<double> strain_thresholds(strain_normal, strain_deviation);

    vector<vector<Point*>> points;
    points.reserve(dim);
    for (size_t i = 0; i < dim; ++i)
        points.push_back({});
    list<Point*> edge_points;
    list<Spring*> springs;

    for (size_t h = 0; h < dim; ++h) {
        for (size_t w = 0; w < dim; ++w) {
            pair<double,double> pos = calc_square_position(w, h, dim, field_size);
            points[h].push_back(new Point(pos));
            if (h == 0 || h == dim-1 || w == 0 || w == dim-1)
                edge_points.push_back(points[h][w]);
        }
    }

    for (size_t h = 0; h < dim; ++h) {
        for (size_t w = 0; w < dim; ++w) {
            // TODO: norm dist
            //double strain_threshold = calc_norm(strain_normal, strain_deviation);
            if (h != dim-1)
                springs.push_back(new Spring(1.0, strain_thresholds(gen), points[h][w], points[h+1][w]));
            if (w != dim-1)
                springs.push_back(new Spring(1.0, strain_thresholds(gen), points[h][w], points[h][w+1]));
        }
    }

    vector<Point*> points1d;
    for (vector<Point*> pointRow : points)
        for (Point* point : pointRow)
            points1d.emplace_back(point);
    return new Grid(start_lambda, points1d, edge_points, springs);
}

void print_grid(Grid *g)
{
    cout << "Printing grid: " << g->points.size() << " points" << endl;
    for (auto p : g->points) {
        if (p == nullptr) {
            cout << "null point in grid" << endl;
            exit(1);
        }
        cout << p->pos.first << " " << p->pos.second << endl;
    }
}
