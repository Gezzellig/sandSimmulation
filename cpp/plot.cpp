#include "gnuplot.h"
#include "point.h"
#include "spring.h"

using namespace std;

vector<Position> getPosNeighbours(Point* point)
{
    vector<Position> posNeighbours;
    for (Spring* spring : point->springs)
    {
        posNeighbours.emplace_back(spring->)
    }
}

string pointToPolygonString(Point* point)
{
    point.
}


int main(){
    GnuplotPipe gp;
    vector<Point> points;
    points.emplace_back(Point(make_pair(2,2)));
    points.emplace_back(Point(make_pair(1,3)));
    points.emplace_back(Point(make_pair(4,5)));
    points.emplace_back(Point(make_pair(0,10)));

    string plotString = "set title 'Simple demo of scatter data conversion to grid data'\n";

    plotString += "set object 1 polygon from ";
    bool first = true;
    for (Point point : points)
    {
        if (first) {
            first = false;

        } else {
            plotString += " to ";
        }
        plotString += to_string(point.pos.first) + ", " + to_string(point.pos.second);
    }
    //To close the polygon
    plotString += " to " + to_string(points[0].pos.first) + ", " + to_string(points[0].pos.second) + "\n";
    plotString += "plot 1, 10\n";
    gp.sendLine(plotString);
    return 0;
}