#include "point.h"
#include "spring.h"

using namespace std;

Point::Point(double x, double y)
: pos(make_pair(x, y)), next_point(nullptr), springs(list<Spring*>())
{
    
}

void Point::add_spring(Spring *spring)
{
    springs.emplace_back(spring);
}

void Point::add_next_point(Point *point)
{
    next_point = point;
}