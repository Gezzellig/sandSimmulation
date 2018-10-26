import random

import numpy as np
import sys

import squareGrid
import hexGrid
import tryGrid
from classes import Grid, Point, Spring
from plot import plot_grid, show_plot, prepare_storage, store_plot, write_settings, FolderAllreadyExistsException, \
    check_storage, plot_strings_against_time
import math


def calc_magnitude(vector):
    """
    Calculates the magnitude(length) of a vector.

    :param vector: The vector of which the magnitude has to be calculated.
    :return: Magnitude of the vector.
    """
    x, y = vector
    return math.sqrt(x ** 2 + y ** 2)


def calc_force_spring(spring, point, lambda_val):
    """
    Calculates the force that this spring applies on the given point.

    :param spring: The spring that applies the force.
    :param point: The given point.
    :param lambda_val: The current lambda value.
    :return: The force in a 2d vector.
    """
    k = spring.springconstant
    if spring.point1 == point:
        point_x, point_y = spring.point1.position
        other_point_x, other_point_y = spring.point2.position
    else:
        point_x, point_y = spring.point2.position
        other_point_x, other_point_y = spring.point1.position
    magnitude = math.sqrt((point_x - other_point_x) ** 2 + (point_y - other_point_y) ** 2)
    force_x = k * ((point_x - other_point_x) / magnitude) * (magnitude - lambda_val)
    force_y = k * ((point_y - other_point_y) / magnitude) * (magnitude - lambda_val)
    return force_x, force_y


def calc_force(point, lambda_val):
    """
    Calculate the force as a 2d vector that is applied on a given point by its springs.

    :param point: The given point .
    :param lambda_val: The current lambda value.
    :return: The force in a 2d vector.
    """
    force_x = 0.0
    force_y = 0.0
    for spring in point.springs:
        cur_force_x, cur_force_y = calc_force_spring(spring, point, lambda_val)
        force_x += cur_force_x
        force_y += cur_force_y
    return -force_x, -force_y


def relax_point(point, lambda_val, mu, move_factor):
    """
    Relax a point by first calculating the force applied on this point, and then checking if this exceeds the minimal
    force threshold mu. A new point is always created and returned to ensure that the calculation is performed on the
    previous grid.

    :param point: The point that has to be relexad.
    :param lambda_val: The current lambda value
    :param mu: The force threshold for movement
    :param move_factor: The amount the point is allowed to move.
    :return: The new version of the point for the relaxed grid.
    """
    move_x, move_y = calc_force(point, lambda_val)
    if calc_magnitude((move_x, move_y)) > mu:
        x, y = point.position
        relaxed_position = (x + (move_x * move_factor), y + move_y * move_factor)
        relaxed_point = Point(relaxed_position)
    else:
        relaxed_point = Point(point.position)
    point.add_next_point(relaxed_point)
    return relaxed_point


def reconnect_grid(prev_grid):
    """
    When all the points are relaxed the knowledge about how springs connect them can't be transfered yet, because some
    points might not yet be initialized for the relaxed grid. Therefore this function loops over all the springs of the
    previous grid and copies all the springs to the appropriate new points.

    The second part of this function ensures that the references between grids are removed to allow the reference
    counter of python to be certain that the memory is not used anymore.

    :param prev_grid: The original grid before it was relaxed.
    :return: List of springs that are present in the relaxed grid.
    """
    springs = list()
    for spring in prev_grid.springs:
        point1 = spring.point1.next_point
        point2 = spring.point2.next_point
        springs.append(Spring(spring.springconstant, spring.strain_threshold, point1, point2))

    # disconnect from previous grid
    for point in prev_grid.points:
        point.next_point = None
    for edge_point in prev_grid.edge_points:
        edge_point.next_point = None
    return springs


def relax_grid(grid, mu, move_factor):
    """
    Relaxes a given grid by relaxing each individual point and then reconnect them using the reconnect_grid.
    This function creates a new grid, so that the old one is preserved for visualization.

    :param grid: The given grid that has to be relaxed.
    :param mu: The force threshold for movement
    :param move_factor: The amount the point is allowed to move.
    :return:
    """
    lambda_val = grid.lambda_val
    relaxed_grid = Grid(lambda_val, list(), list(), list())
    for edge_point in grid.edge_points:
        new_edge_point = Point(edge_point.position)
        edge_point.add_next_point(new_edge_point)
        relaxed_grid.edge_points.append(new_edge_point)
    for point in grid.points:
        relaxed_grid.points.append(relax_point(point, lambda_val, mu, move_factor))
    relaxed_grid.springs = reconnect_grid(grid)
    return relaxed_grid


def relax_grid_n_times(grid, n, mu, move_factor):
    """
    Relax a grid n times.

    :param grid: The grid that has to be relaxed.
    :param n: The amount of times the grid has to be relaxed
    :param mu: The force threshold for movement
    :param move_factor: The amount the point is allowed to move.
    :return: The relaxed grid.
    """
    for i in range(0, n):
        grid = relax_grid(grid, mu, move_factor)
    return grid


def calc_strain(spring, lambda_val):
    """
    Calculate the strain that is applied on a spring.

    :param spring: The spring.
    :param lambda_val: The current lambda value.
    :return: The strain that is applied.
    """
    point1_x, point1_y = spring.point1.position
    point2_x, point2_y = spring.point2.position
    magnitude = calc_magnitude((point1_x - point2_x, point1_y - point2_y))
    return magnitude / lambda_val - 1


def max_strain_spring(grid):
    """
    Finds for a grid the spring that currently endures the largest relative strain.
    If all the springs in a grid endure a negative relative strain None is returned, because no spring should break.

    :param grid: The grid that contains all the springs.
    :return: The spring that endures the largest relative strain. If none are positive return None
    """
    max_rel_strain = 0
    max_rel_strain_spring = None
    for spring in grid.springs:
        rel_strain = calc_strain(spring, grid.lambda_val) - spring.strain_threshold
        if rel_strain > max_rel_strain:
            max_rel_strain = rel_strain
            max_rel_strain_spring = spring
    return max_rel_strain_spring


def spring_break_loop(grid, n, mu, move_factor):
    """
    While a spring keeps breaking relax the grid n times.

    :param grid: The applicable grid.
    :param n: The amount of times the grid is relaxed when it has to be.
    :param mu: The force threshold for movement.
    :param move_factor: The amount the point is allowed to move.
    :return: The relaxed grid after zero or multiple spring breaks.
    """
    relaxed_grid = relax_grid_n_times(grid, n, mu, move_factor)
    broken_spring = max_strain_spring(relaxed_grid)
    while broken_spring is not None:
        relaxed_grid.remove_spring(broken_spring)
        relaxed_grid = relax_grid_n_times(relaxed_grid, n, mu, move_factor)
        broken_spring = max_strain_spring(relaxed_grid)
    return relaxed_grid


def decrease_lambda(grid, decrement_step_size):
    """
    Creates a copy of the given grid and for this decreases the lambda value by the decrement_step_size.

    :param grid: The given grid.
    :param decrement_step_size: The amount lambda has to be decreased.
    :return: A copy of the given grid, where the lambda value is decreased.
    """
    lambda_val = grid.lambda_val - decrement_step_size
    decreased_grid = Grid(lambda_val, list(), list(), list())
    for edge_point in grid.edge_points:
        new_edge_point = Point(edge_point.position)
        edge_point.add_next_point(new_edge_point)
        decreased_grid.edge_points.append(new_edge_point)
    for point in grid.points:
        new_point = Point(point.position)
        point.add_next_point(new_point)
        decreased_grid.points.append(new_point)
    decreased_grid.springs = reconnect_grid(grid)
    return decreased_grid


def decrease_lambda_loop(grid, min_lambda, decrement_step_size, n, mu, move_factor):
    """
    Startpoint point of the actual simulation.
    While lambda is still larger than the min_lambda value dececrease the lambda value and perform the spring_break_loop

    :param grid: The grid that has to be used for the simulation.
    :param min_lambda: The stop value of lambda.
    :param decrement_step_size: The amount lambda has to be decreased every step.
    :param n: The amount of times the grid is relaxed when it has to be.
    :param mu: The force threshold for movement.
    :param move_factor: The amount the point is allowed to move.
    :return: The final grid that is the result after lambda is smaller than the minimum value. And all intermediate
    grids of each time lambda was decreased, which can be used for visualization.
    """
    intermediate_grids = list()
    decreased_grid = decrease_lambda(grid, decrement_step_size)
    while decreased_grid.lambda_val > min_lambda:
        print("Cur lambda= {}".format(decreased_grid.lambda_val))
        spring_snapped_grid = spring_break_loop(decreased_grid, n, mu, move_factor)
        intermediate_grids.append(spring_snapped_grid)
        decreased_grid = decrease_lambda(spring_snapped_grid, decrement_step_size)
    return decreased_grid, intermediate_grids


def sand_simulation(folder_name, type_string, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, min_lambda, decrement_step_size, n, mu, move_factor):
    """
    Wrapper function that initializes all resources needed for the simulation and then executes the simulation itself.

    :param folder_name:
    :param type_string: A string defining which grid type has to be used, Options: square, hex
    :param dim: The width of the grid that has to be created.
    :param springconstant_normal: The normal of the springconstant.
    :param springconstant_deviation: The deviation of the springconstant on this normal.
    :param strain_normal: The normal of the strain.
    :param strain_deviation: The deviation of the strain on this normal.
    :param min_lambda: The stop value of lambda.
    :param decrement_step_size: The amount lambda has to be decreased every step.
    :param n: The amount of times the grid is relaxed when it has to be.
    :param mu: The force threshold for movement.
    :param move_factor: The amount the point is allowed to move.
    :return:
    """
    start_grid = None

    random.seed(12345)

    if type_string == "square":
        start_grid = squareGrid.create_square_grid(dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation)
    elif type_string == "hex":
        start_grid = hexGrid.create_hex_point_grid(dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation)
    if start_grid == None:
        print("No grid type was specified, exiting the program")
        raise Exception

    try:
        check_storage(folder_name)
        print("Starting simulation of: {}".format(folder_name))

        #The actual call of the simulation
        grid, intermediate_grids = decrease_lambda_loop(start_grid, min_lambda, decrement_step_size, n, mu, move_factor)

        print("output time of: {}".format(folder_name))
        total_folder_name = prepare_storage(folder_name)
        write_settings(total_folder_name, type_string, dim, strain_normal, strain_deviation, min_lambda, decrement_step_size, n, mu, move_factor)

        for inter_grid in intermediate_grids:
            store_plot(total_folder_name, inter_grid)
        store_plot(total_folder_name, grid)
        return [start_grid] + intermediate_grids + [grid]
    except FolderAllreadyExistsException:
        print("The folder already existed for: {} skipping this entry".format(folder_name))


