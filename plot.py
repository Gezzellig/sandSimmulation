import math
import os

import matplotlib.pyplot as plt
import matplotlib.collections as mat_col


def get_xs_ys(points):
    xs = list()
    ys = list()
    for point in points:
        x, y = point.position
        xs.append(x)
        ys.append(y)
    return xs, ys


def plot_spring(spring):
    point1_x, point1_y = spring.point1.position
    point2_x, point2_y = spring.point2.position
    plt.plot([point1_x, point2_x], [point1_y, point2_y], color='k', linestyle='-', zorder=1)


def plot_springs(grid):
    for spring in grid.springs:
        plot_spring(spring)


def plot_forces(grid):
    from sandSimulation import calc_force
    for point in grid.points:
        x, y = point.position
        force_x, force_y = calc_force(point, grid.lambda_val)
        plt.arrow(x, y, force_x, force_y)


def plot_points(grid):
    points = grid.points
    xs, ys = get_xs_ys(points)
    plt.scatter(xs, ys, color="r", zorder=2)


def plot_edge_points(grid):
    edge_points = grid.edge_points
    xs, ys = get_xs_ys(edge_points)
    plt.scatter(xs, ys, color="b", zorder=2)


def order_neighbours_in_circle(point, neighbours_pos):
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


def plot_triangles(ax, grid):
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
    fig, ax = plt.subplots()
    fig.suptitle("Points:{}, Lambda={:3.3f}".format(len(grid.points), grid.lambda_val))
    #plot_points(grid)
    #plot_springs(grid)
    plot_triangles(ax, grid)
    plot_edge_points(grid)
    #plot_forces(grid)


def prepare_storage(folder_name):
    base_folder_name = "plots"
    if not os.path.exists(base_folder_name):
        os.makedirs(base_folder_name)
    total_folder_name = "{}/{}".format(base_folder_name, folder_name)
    if os.path.exists(total_folder_name):
        print("The output folder already exists!")
        exit(-1)
    os.makedirs(total_folder_name)
    return total_folder_name

def write_settings(total_folder_name, type_string, vertical_size, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor):
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
    if total_folder_name == "":
        print("Trying to store a plot, but prepare_storage isn't called!")
        exit(-1)
    image_name = "p{}l{:3.3f}".format(len(grid.points), grid.lambda_val).replace(".", "")
    plot_grid(grid)
    plt.savefig("{}/{}.png".format(total_folder_name, image_name), bbox_inches="tight")
    plt.close()


def show_plot():
    plt.show()
