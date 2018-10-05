#ifndef SPRING_H
#define SPRING_H

struct Point;

struct Spring
{
    double springconstant;
    double strain_threshold;
    Point *a, *b;

    Spring(double springconstant, double strain_threshold, Point *a, Point *b);
    Point* getOtherPoint(Point* point);

};

#endif
