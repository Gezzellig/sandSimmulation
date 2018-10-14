import random

import numpy as np
import sys

import squareGrid
import hexGrid
from classes import Grid, Point, Spring
from plot import plot_grid, show_plot, prepare_storage, store_plot, write_settings
import math


def calc_magnitude(vector):
    x, y = vector
    return math.sqrt(x ** 2 + y ** 2)


def calc_force_spring(spring, point, lambda_val):
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
    force_x = 0.0
    force_y = 0.0
    for spring in point.springs:
        cur_force_x, cur_force_y = calc_force_spring(spring, point, lambda_val)
        force_x += cur_force_x
        force_y += cur_force_y
    return -force_x, -force_y


def relax_point(point, lambda_val, mu, move_factor):
    move_x, move_y = calc_force(point, lambda_val)
    if calc_magnitude((move_x, move_y)) > mu:
        x, y = point.position
        relaxed_position = (x + (move_x * move_factor), y + move_y * move_factor)
        relaxed_point = Point(relaxed_position)
    else:
        relaxed_point = Point(point.position)
    point.add_next_point(relaxed_point)
    return relaxed_point


def reconnect_grid(grid):
    springs = list()
    for spring in grid.springs:
        point1 = spring.point1.next_point
        point2 = spring.point2.next_point
        springs.append(Spring(spring.springconstant, spring.strain_threshold, point1, point2))

    # disconnect from previous grid
    for point in grid.points:
        point.next_point = None
    for edge_point in grid.edge_points:
        edge_point.next_point = None
    return springs


def relax_grid(grid, mu, move_factor):
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
    for i in range(0, n):
        grid = relax_grid(grid, mu, move_factor)
    return grid


def calc_strain(spring, lambda_val):
    point1_x, point1_y = spring.point1.position
    point2_x, point2_y = spring.point2.position
    magnitude = calc_magnitude((point1_x - point2_x, point1_y - point2_y))
    return magnitude / lambda_val - 1


def max_strain_spring(grid):
    max_rel_strain = 0
    max_rel_strain_spring = None
    for spring in grid.springs:
        rel_strain = calc_strain(spring, grid.lambda_val) - spring.strain_threshold
        if rel_strain > max_rel_strain:
            max_rel_strain = rel_strain
            max_rel_strain_spring = spring
    return max_rel_strain_spring


def spring_break_loop(grid, relax_iterations, mu, move_factor):
    relaxed_grid = relax_grid_n_times(grid, relax_iterations, mu, move_factor)
    broken_spring = max_strain_spring(relaxed_grid)
    while broken_spring is not None:
        relaxed_grid.remove_spring(broken_spring)
        relaxed_grid = relax_grid_n_times(relaxed_grid, relax_iterations, mu, move_factor)
        broken_spring = max_strain_spring(relaxed_grid)
    return relaxed_grid


def decrease_lambda(grid, decrement_step_size):
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


def decrease_lambda_loop(grid, min_lambda, decrement_step_size, relax_iterations, mu, move_factor):
    intermediate_grids = list()
    decreased_grid = decrease_lambda(grid, decrement_step_size)
    while decreased_grid.lambda_val > min_lambda:
        print("Cur lambda= {}".format(decreased_grid.lambda_val))
        spring_snapped_grid = spring_break_loop(decreased_grid, relax_iterations, mu, move_factor)
        intermediate_grids.append(spring_snapped_grid)
        decreased_grid = decrease_lambda(spring_snapped_grid, decrement_step_size)
    return decreased_grid, intermediate_grids


def sand_simulation(folder_name, type_string, dim, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor):
    grid = None

    random.seed(12345)

    if type_string == "square":
        grid = squareGrid.create_square_grid(dim, strain_normal, strain_deviation)
    elif type_string == "hex":
        grid = hexGrid.create_hex_point_grid(dim, strain_normal, strain_deviation)

    if grid == None:
        print("No grid type was specified, exiting the program")
        exit(-1)
    total_folder_name = prepare_storage(folder_name)
    write_settings(total_folder_name, type_string, dim, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor)

    print("Starting simulation of: {}".format(total_folder_name))

    #The actual call of the simulation
    grid, intermediate_grids = decrease_lambda_loop(grid, min_lambda, decrement_step_size, relax_iterations, mu, move_factor)

    print("output time of: {}".format(total_folder_name))
    for inter_grid in intermediate_grids:
        store_plot(total_folder_name, inter_grid)
    store_plot(total_folder_name, grid)
