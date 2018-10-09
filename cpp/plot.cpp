#include "gnuplot.h"
#include "point.h"
#include "spring.h"
#include "grid.h"

using namespace std;

vector<Point*> getNeighbours(Point* point)
{
    vector<Point*> neighbours;
    for (Spring* spring : point->springs)
    {
        neighbours.emplace_back(spring->getOtherPoint(point));
    }
    return neighbours;
}

string pointToPolygonString(int objectCount, Point* point)
{
    vector<Point*> neighbours = getNeighbours(point);
    if (neighbours.size() < 2)
        return "";

    string polygonString = "set object " + to_string(objectCount) + " polygon from ";
    bool first = true;
    for (Point* neighbour : neighbours)
    {
        if (first)
            first = false;
        else
            polygonString += " to ";
        polygonString += to_string(neighbour->pos.first) + ", " + to_string(neighbour->pos.second);
    }
    //To close the polygon
    polygonString += " to " + to_string(neighbours[0]->pos.first) + ", " + to_string(neighbours[0]->pos.second) + "\n";
    return polygonString;
}


void plot_grid(Grid *grid) {
    GnuplotPipe gp;

    string plotString = "set title 'Simple demo of scatter data conversion to grid data'\n";
    int cnt = 1;

    for (Point* point : grid->points)
    {
        plotString += pointToPolygonString(cnt, point);
        cnt++;
    }

    cout << "Points:" << grid->points.size() << " springs:" << grid->springs.size();

    plotString += "plot 0, 10\n";
    cout << plotString;
    gp.sendLine(plotString);
}
