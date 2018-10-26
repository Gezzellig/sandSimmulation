import math
import os

import matplotlib.pyplot as plt
import matplotlib.collections as mat_col

class FolderAllreadyExistsException(Exception):
    pass

def get_xs_ys(points):
    """
    Transform a list of points to two lists containing their x and y locations.

    :param points: The list of points
    :return: The two lists of x and y coordinates
    """
    xs = list()
    ys = list()
    for point in points:
        x, y = point.position
        xs.append(x)
        ys.append(y)
    return xs, ys


def plot_spring(spring):
    """
    Plots a simple line representing a spring.

    :param spring: The spring
    """
    point1_x, point1_y = spring.point1.position
    point2_x, point2_y = spring.point2.position
    plt.plot([point1_x, point2_x], [point1_y, point2_y], color='k', linestyle='-', zorder=1)


def plot_springs(grid):
    """
    Plots all the springs in a grid.

    :param grid: The grid that holds the springs.
    """
    for spring in grid.springs:
        plot_spring(spring)


def plot_forces(grid):
    """
    Plot all the forces as arrows of a grid

    :param grid: The grid
    """
    from sandSimulation import calc_force
    for point in grid.points:
        x, y = point.position
        force_x, force_y = calc_force(point, grid.lambda_val)
        plt.arrow(x, y, force_x, force_y)


def plot_points(grid):
    """
    Plot all points of a grid as red dots.

    :param grid: The grid
    """
    points = grid.points
    xs, ys = get_xs_ys(points)
    plt.scatter(xs, ys, color="r", zorder=2)


def plot_edge_points(grid):
    """
    Plot all edge points of a grid as blue dots.

    :param grid: the grid
    """
    edge_points = grid.edge_points
    xs, ys = get_xs_ys(edge_points)
    plt.scatter(xs, ys, color="b", zorder=2)


def order_neighbours_in_circle(point, neighbours_pos):
    """
    Takes a list of neighbours and a center point and orders them in a circle.
    This is necessary so the polygon plotting creates nice areas instead of crossing bowties.

    :param point: The center point
    :param neighbours_pos: The positions of the neighbours.
    :return: The coordinates of the neighbours in order.
    """
    angle_coordinate_pairs = list()
    point_x, point_y = point.position
    for pos in neighbours_pos:
        x, y = pos
        angle = math.atan2(point_y - y, point_x - x)
        angle_coordinate_pairs.append((angle, x, y))
    inorder_coordinates = list()
    sorted_pairs = sorted(angle_coordinate_pairs, key=lambda pair: pair[0])
    for pair in sorted_pairs:
        angle, x, y = pair
        inorder_coordinates.append([x, y])
    return inorder_coordinates


def plot_polygons(ax, grid):
    """
    Plot a polygon for each point covering its neighbours.

    :param ax: The plot in which the polygons should be added.
    :param grid: The grid containing all the points.
    """
    patches = list()
    for point in grid.points:
        neighbours_pos = list()
        for spring in point.springs:
            point_x, point_y = spring.other_point(point).position
            neighbours_pos.append([point_x, point_y])
            inorder_coordinates = order_neighbours_in_circle(point, neighbours_pos)
            if len(inorder_coordinates) > 1:
                polygon = plt.Polygon(inorder_coordinates, True)
                patches.append(polygon)
    ax.add_collection(mat_col.PatchCollection(patches))


def plot_grid(grid):
    """
    Plot a grid.
    Different plot styles can be achieved by commenting out lines below.
    Standard plots only contain edge points and the polygons.
    :param grid: The grid that has to be plotted.
    """
    fig, ax = plt.subplots()
    #fig.suptitle("Points:{}, Lambda={:3.3f}".format(len(grid.points), grid.lambda_val))
    #plot_points(grid)
    #plot_springs(grid)
    plot_polygons(ax, grid)
    plot_edge_points(grid)
    #plot_forces(grid)


def check_storage(folder_name):
    """
    Check if the folder already exists, indicating that this simulation has already ran.

    :param folder_name: The name of folder where the results of the simulation have to be stored.
    """
    base_folder_name = "plots"
    total_folder_name = "{}/{}".format(base_folder_name, folder_name)
    if os.path.exists(total_folder_name):
        raise FolderAllreadyExistsException("The output folder already exists!")


def prepare_storage(folder_name):
    """
    Create the folders needed to store the plots.

    :param folder_name: The name of folder where the results of the simulation have to be stored.
    :return: the real path where everything has to be stored.
    """
    base_folder_name = "plots"
    if not os.path.exists(base_folder_name):
        os.makedirs(base_folder_name)
    total_folder_name = "{}/{}".format(base_folder_name, folder_name)
    if os.path.exists(total_folder_name):
        raise FolderAllreadyExistsException("The output folder already exists!")
    os.makedirs(total_folder_name)
    return total_folder_name

def write_settings(total_folder_name, type_string, vertical_size, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor):
    """
    A simple function that writes all the settings to a file for later inspection.
    """
    file = open("{}/runsettings.txt".format(total_folder_name), "w")
    file.write("type_string: {}\n".format(type_string))
    file.write("dim: {}\n".format(vertical_size))
    file.write("strain_normal: {}\n".format(strain_normal))
    file.write("strain_deviation: {}\n".format(strain_deviation))
    file.write("min_lambda: {}\n".format(min_lambda))
    file.write("decrement_step_size: {}\n".format(decrement_step_size))
    file.write("relax_iterations: {}\n".format(relax_iterations))
    file.write("mu: {}\n".format(mu))
    file.write("move_factor: {}\n".format(move_factor))
    file.close()

def store_plot(total_folder_name, grid):
    """
    Creates and stores the plot as an png and then removes it from execution memory.

    :param total_folder_name: Location where the plot has to be stored.
    :param grid: The grid that is being stored.
    """
    if total_folder_name == "":
        print("Trying to store a plot, but prepare_storage isn't called!")
        raise Exception
    image_name = "lam{:3.3f}".format(grid.lambda_val).replace(".", "")
    plot_grid(grid)
    plt.savefig("{}/{}.png".format(total_folder_name, image_name), bbox_inches="tight")
    plt.close()

def plot_strings_against_time(ax, grids, value):
    """
    Visualize the amount of springs versus the time.
    This is a meta plot that has to be executed using multiple executions of the simulation.

    :param ax: The plot that is used.
    :param grids: The grids that have to be plotted
    :param value: The label of the line that is added by this function.
    """
    xs = list()
    ys = list()
    for grid in grids:
        xs.append(grid.lambda_val)
        ys.append(len(grid.springs))
    return ax.plot(xs, ys, label="{:.3}".format(value))

def store_plot_strings(base_folder_name, legend_text):
    """
    Wrapper function to store the plot of springs
    """
    image_name = "{}_springs".format(legend_text)
    plt.savefig("plots/{}/{}.png".format(base_folder_name, image_name), bbox_inches="tight")
    plt.close()

def plot_all_strings_against_time(all_grids, legend_text, alternating_values, total_folder_name):
    """
    Function that uses multiple executions of the simulation to plot all the results in one figure.

    :param all_grids: a list of lists of grids where every entry is one whole simulation.
    :param legend_text: The text that should be displayed in legend.
    :param alternating_values: The value that is changed between different executions of the simulation
    :param total_folder_name: The location where the plot has to be stored.
    """
    f, ax = plt.subplots(1)
    for grids, value in zip(all_grids, alternating_values):
        plot_strings_against_time(ax, grids, value)
    plt.legend(title=legend_text)
    plt.gca().invert_xaxis()
    plt.xlabel("Lambda")
    plt.ylabel("Number of springs")
    store_plot_strings(total_folder_name, legend_text)

def show_plot():
    """
    Display all the plots currently in memory.
    """
    plt.show()
