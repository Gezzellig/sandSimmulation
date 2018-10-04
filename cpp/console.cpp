#include <iostream>
#include "grid.h"
#include "sandSimulation.h"

using namespace std;

int main(int argc, char *argv[])
{
    cout << "sand simulation" << endl;

    Grid initial_grid = create_square_grid(20, 50.0, 0.25, 0.1);

    print_grid(&initial_grid);

    Grid final = decrease_lambda_loop(initial_grid, 0.75, 0.025, 5, 0.01, 0.2);

    print_grid(&final);

    return 0;
}
