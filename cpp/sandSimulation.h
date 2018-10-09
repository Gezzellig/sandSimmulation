#ifndef SANDSIM_H
#define SANDSIM_H

#include "grid.h"

list<Grid*> decrease_lambda_loop(Grid *grid, double min_lambda, double decrement_step_size, size_t n, double mu, double move_factor);

#endif
