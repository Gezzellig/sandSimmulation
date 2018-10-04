
#include <utility>
#include <math.h>
#include <iostream>
#include "point.h"
#include "spring.h"
#include "grid.h"

using namespace std;

double calc_magnitude(pair<double, double> vector)
{
    return sqrt(pow(vector.first, 2) + pow(vector.second, 2));
}

pair<double, double> calc_force_spring(Spring *spring, Point *point, double lambda_val)
{
    double point_x, point_y, other_point_x, other_point_y;
    double k = spring->springconstant;
    //CHECK IF CORRECT COMPARISON
    if (spring->a == point)
    {
        point_x = spring->a->pos.first;
        point_y = spring->a->pos.second;
        other_point_x = spring->b->pos.first;
        other_point_y = spring->b->pos.second;
    }
    else
    {
        point_x = spring->b->pos.first;
        point_y = spring->b->pos.second;
        other_point_x = spring->a->pos.first;
        other_point_y = spring->a->pos.second;
    }
    double magnitude = calc_magnitude(make_pair(point_x - other_point_x, point_y - other_point_y));
    double force_x = k*((point_x - other_point_x) / magnitude) * (magnitude - lambda_val);
    double force_y = k*((point_y - other_point_y) / magnitude) * (magnitude - lambda_val);
    return make_pair(force_x, force_y);
}

pair<double, double> calc_force(Point *point, double lambda_val)
{
    double force_x = 0.0;
    double force_y = 0.0;
    for (Spring* spring_ptr : point->springs)
    {
        pair<double, double> cur_forces = calc_force_spring(spring_ptr, point, lambda_val);
        force_x += cur_forces.first;
        force_y += cur_forces.second;
    }
    return make_pair(-force_x, -force_y);
}


//Something fixed with pointers and copyconstructor stuffffff
Point *relax_point(Point *point, double lambda_val, double mu, double move_factor)
{
    pair<double, double> moves = calc_force(point, lambda_val);
    Position new_position = {0,0};
    if (calc_magnitude(moves) > mu)
    {
        double pos_x = point->pos.first;
        double move_x = moves.first;
        double relaxed_x = pos_x + (move_x * move_factor);
        double pos_y = point->pos.second;
        double move_y = moves.second;
        double relaxed_y = pos_y + (move_y * move_factor);
        new_position = make_pair(relaxed_x, relaxed_y);
    }
    else
    {
        new_position = point->pos;
    }
    Point *relaxed_point = new Point(new_position);
    point->add_next_point(relaxed_point);
    return relaxed_point;
}

list<Spring*> reconnect_grid(Grid grid)
{
    list<Spring*> new_springs = list<Spring*>();
    for (Spring *spring : grid.springs) {
        Point* a = spring->a->next_point;
        Point* b = spring->b->next_point;
        new_springs.emplace_back(new Spring(spring->springconstant, spring->springconstant, a, b));
    }
    return new_springs;

    //Still have to add disconnect stuff
}

Grid relax_grid(Grid grid, double mu, double move_factor)
{
    double lambda_val = grid.lambda_val;
    Grid relaxed_grid(lambda_val);
//    for (Point *edge_point : grid.edge_points)
//    {
//        Point *new_edge_point = new Point(edge_point->pos);
//        edge_point->add_next_point(new_edge_point);
//        relaxed_grid->edge_points.push_back(*new_edge_point);
//    }
    for (size_t h = 0; h < grid.points.size(); ++h)
    {
        for (Point *p : grid.points[h]) {
            relaxed_grid.points[h].push_back(relax_point(p, lambda_val, mu, move_factor));
        }
    }
    relaxed_grid.springs = reconnect_grid(grid);
    return relaxed_grid;
}

Grid relax_grid_n_times(Grid grid, size_t n, double mu, double move_factor)
{
    for (size_t i = 0; i<n; i++)
    {
        grid = relax_grid(grid, mu, move_factor);
    }
    return grid;
}

double calc_strain(Spring spring, double lambda_val)
{
    double a_x = spring.a->pos.first;
    double a_y = spring.a->pos.second;
    double b_x = spring.b->pos.first;
    double b_y = spring.b->pos.second;
    double magnitude = calc_magnitude(make_pair(a_x-b_x, a_y-b_y));
    return magnitude / lambda_val - 1;
}

Spring *max_strain_spring(Grid grid)
{
    double max_rel_strain = 0;
    Spring *max_rel_strain_spring = nullptr;
    for (Spring *spring : grid.springs)
    {
        double rel_strain = calc_strain(*spring, grid.lambda_val);
        if (rel_strain > max_rel_strain)
        {
            max_rel_strain = rel_strain;
            max_rel_strain_spring = spring;
        }
    }
    return max_rel_strain_spring;
}

Grid spring_break_loop(Grid grid, size_t n, double mu, double move_factor)
{
    Grid relaxed_grid = relax_grid_n_times(grid, n, mu, move_factor);
    Spring *broken_spring = max_strain_spring(relaxed_grid);
    while (broken_spring != nullptr)
    {
        relaxed_grid.remove_spring(broken_spring);
        relaxed_grid = relax_grid_n_times(relaxed_grid, n, mu, move_factor);
        broken_spring = max_strain_spring(relaxed_grid);
    }
    return relaxed_grid;
}


//Maybe later want to create a new grid when lambda is reduced, for visualization
Grid decrease_lambda_loop(Grid grid, double min_lambda, double decrement_step_size, size_t n, double mu, double move_factor)
{
    grid.lambda_val -= decrement_step_size;
    while (grid.lambda_val > min_lambda)
    {
        cout << "Current Lambda: " << grid.lambda_val;
        grid = spring_break_loop(grid, n, mu, move_factor);
        //Add here some step for visualization perpouses
        grid.lambda_val -= decrement_step_size;
    }
    return grid;
}

//A listing of basic values used in the program.
void normal_val_run()
{
    double strain_normal = 0.25;
    double strain_deviation = 0.2;
    double mu = 0.01;
    double move_factor = 0.2;
    double min_lambda = 0.75;
    double decrement_step_size = 0.025;
    int n = 5; //number of iteration allowed in the relax step.
}
