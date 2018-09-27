#ifndef SPRING_H
#define SPRING_H

#include "point.h"

struct Spring
{
    double springconstant;
    double strain_threshold;
    Point &a, &b;

    Spring(double springconstant, double strain_threshold, Point &a, Point &b);

};

#endif