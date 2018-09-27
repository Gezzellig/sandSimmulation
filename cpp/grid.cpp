
#include <list>
#include "grid.h"
#include "spring.h"

using namespace std;

Grid::Grid(double lambda_val, list<Point> points, list<Point> edge_points, list<Spring*> springs)
: lambda_val(lambda_val), points(points), edge_points(edge_points), springs(springs)
{

}

void Grid::remove_spring(Spring *spring)
{
    springs.remove(spring);
}

