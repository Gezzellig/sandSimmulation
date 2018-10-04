#include <iostream>
#include "grid.h"

using namespace std;

int main(int argc, char *argv[])
{
    cout << "sand simulation" << endl;

    auto g = create_square_grid(20, 50.0, 0.25, 0.1);
    return 0;
}
