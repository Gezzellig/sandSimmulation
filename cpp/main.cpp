#include <iostream>
#include "point.h"

using namespace std;


int main(int argc, char **argv)
{
    Point p(1,1);

    cout << p.pos.first << "," << p.pos.second << endl;

    return 0;
}