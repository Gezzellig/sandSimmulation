#include "spring.h"

#include "point.h"

Spring::Spring(double springconstant, double strain_threshold, Point& a, Point& b)
: springconstant(springconstant), strain_threshold(strain_threshold), a(a), b(b)
{
    a.add_spring(this);
    b.add_spring(this);
}