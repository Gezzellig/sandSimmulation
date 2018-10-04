#ifndef POINT_H
#define POINT_H

#include <list>

using namespace std;
using Position = pair<double, double>;

struct Spring;

struct Point
{
    Position pos;
    Point *next_point;
    list<Spring*> springs;

    Point(Position pos);

    void add_spring(Spring *spring);
    void add_next_point(Point *p);

};

#endif
