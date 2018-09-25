#ifndef POINT_H
#define POINT_H

#include <list>

using namespace std;

struct Spring;

struct Point
{
    pair<double, double> pos;
    Point *next_point;
    list<Spring*> springs;

    Point(double x, double y);

    void add_spring(Spring *spring);
    void add_next_point(Point *p);

};

#endif