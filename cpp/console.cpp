#include <iostream>
#include "grid.h"
#include "sandSimulation.h"
#include "plot.h"

using namespace std;

int main(int argc, char *argv[])
{
    double strain_normal = 0.25;
    double strain_deviation = 0.2;
    double mu = 0.01;
    double move_factor = 0.2;
    double min_lambda = 0.3;
    double decrement_step_size = 0.025;

    size_t n = 5; //number of iteration allowed in the relax step.
    cout << "sand simulation" << endl;

    Grid *initial_grid = create_square_grid(10, 9.0, strain_normal, strain_deviation);
//    print_grid(&initial_grid);

    list<Grid*> intermediate_grids = decrease_lambda_loop(initial_grid, min_lambda,decrement_step_size, n, mu, move_factor);

    plot_grid(intermediate_grids.back());
//    for (Grid *g : intermediate_grids) {
//        if (g != nullptr)
//            delete g;
//    }

    return 0;
}
