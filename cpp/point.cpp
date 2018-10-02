#include "point.h"
#include "spring.h"

using namespace std;

Point::Point(pair<double, double> pos)
: pos(pos), next_point(nullptr)
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