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


int main(){
    GnuplotPipe gp;

    /*Point* centerPoint = new Point(make_pair(2,2));
    Point* point1 = new Point(make_pair(2,4));
    Point* point2 = new Point(make_pair(4,4));
    Point* point3 = new Point(make_pair(0,6));
    Point* point4 = new Point(make_pair(-2,-2));
    Point* point5 = new Point(make_pair(8,0));

    Spring* spring1 = new Spring(1.0, 1.0, centerPoint, point1);
    Spring* spring2 = new Spring(1.0, 1.0, point2, centerPoint);
    Spring* spring3 = new Spring(1.0, 1.0, point3, centerPoint);
    Spring* spring4 = new Spring(1.0, 1.0, centerPoint, point4);
    Spring* spring5 = new Spring(1.0, 1.0, point2, point5);
    Spring* spring6 = new Spring(1.0, 1.0, point2, point3);*/

    Grid grid = create_square_grid(100, 9.0, 1.0, 1.0);
    string plotString = "set title 'Simple demo of scatter data conversion to grid data'\n";
    int cnt = 1;
    for (Point* point : grid.points)
    {
        plotString += pointToPolygonString(cnt, point);
        cnt++;
    }


    //plotString += pointToPolygonString(2, grid.points[14]);

    /*vector<Point> points;
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
    */
//    plotString += "[set xrange=0:100]\n";
    plotString += "plot [0:100][5:7] -10\n";
    cout << plotString;
    gp.sendLine(plotString);
    return 0;
}