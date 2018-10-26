import math
import random

import plot
from classes import Point, Grid, Spring, create_new_spring


def calc_position(h, w):

    offset_x = 0.1
    offset_y = 0.1
    rx = random.uniform(-offset_x, offset_x)
    ry = random.uniform(-offset_y, offset_y)

    x_pos = w * (math.sqrt(2.5) / 2)
    if h % 2 == 0:
        y_pos = 1.5 * h + (w % 2) * 0.5
    else:
        y_pos = 1.5 * h + ((w-1) % 2) * 0.5

    # return x_pos + rx, y_pos + ry
    return x_pos, y_pos


def create_points_try(dim):
    points_grid = list()
    for h in range(0, dim):
        points_grid.append(list())
        for w in range(0, dim):
            points_grid[h].append(Point(calc_position(h, w)))
    return points_grid

def link_points(dim, points_grid, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation):
    springs = list()

    #Horizontal springs
    for h in range(1, dim-1):
        for w in range(0, dim-1):
            springs.append(create_new_spring(springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, points_grid[h][w], points_grid[h][w+1]))

    #Vertical springs
    for h in range(0, dim-1):
        if h % 2 == 0:
            for w in range(1, dim-1, 2):
                springs.append(create_new_spring(springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, points_grid[h][w], points_grid[h+1][w]))
        else:
            for w in range(2, dim-1, 2):
                springs.append(create_new_spring(springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, points_grid[h][w], points_grid[h + 1][w]))
    return springs


def create_try_grid(dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation):
    points_grid = create_points_try(dim)
    springs = link_points(dim, points_grid, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation)


    points = list()
    for h in range(1, len(points_grid) - 1):
        for w in range(1, len(points_grid[h]) - 1):
            points.append(points_grid[h][w])

    edge_points = list()
    for h in range(1, len(points_grid) - 1):
        edge_points.append(points_grid[h][0])
        edge_points.append(points_grid[h][-1])

    for w in range(1, len(points_grid[0]) - 1, 2):
        edge_points.append(points_grid[0][w])
        if dim % 2 == 0:
            edge_points.append(points_grid[-1][w])
        else:
            if not w == dim-2:
                edge_points.append(points_grid[-1][w+1])
    return Grid(1, points, edge_points, springs)