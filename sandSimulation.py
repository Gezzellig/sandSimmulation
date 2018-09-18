import sqaureGrid
from classes import Grid, Point, Spring
from plot import plot_grid, show_plot
import math


def calc_magnitude(vector):
	x, y = vector
	return math.sqrt(x**2 + y**2)


def calc_force_spring(spring, point, lambda_val):
	k = spring.springconstant
	if spring.point1 == point:
		point_x, point_y = spring.point1.position
		other_point_x, other_point_y = spring.point2.position
	else:
		point_x, point_y = spring.point2.position
		other_point_x, other_point_y = spring.point1.position
	magnitude = math.sqrt((point_x - other_point_x)**2 + (point_y - other_point_y)**2)
	force_x = k*((point_x - other_point_x) / magnitude) * (magnitude - lambda_val)
	force_y = k*((point_y - other_point_y) / magnitude) * (magnitude - lambda_val)
	return force_x, force_y
	
	
def calc_force(point, lambda_val):
	force_x = 0.0
	force_y = 0.0
	for spring in point.springs:
		cur_force_x, cur_force_y = calc_force_spring(spring, point, lambda_val)
		force_x += cur_force_x
		force_y += cur_force_y
	return -force_x, -force_y


def relax_point(point, lambda_val):
	move_x, move_y = calc_force(point, lambda_val)
	if calc_magnitude((move_x, move_y)) > mu:
		x, y = point.position
		relaxed_position = (x + (move_x*0.1), y + move_y*0.1)
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
	return springs
			

def relax_grid(grid):
	lambda_val = grid.lambda_val
	relaxed_grid = Grid(lambda_val, list(), list(), list())
	for edge_point in grid.edge_points:
		new_edge_point = Point(edge_point.position)
		edge_point.add_next_point(new_edge_point)
		relaxed_grid.edge_points.append(new_edge_point)
	for point in grid.points:
		relaxed_grid.points.append(relax_point(point, lambda_val))
	relaxed_grid.springs = reconnect_grid(grid)
	return relaxed_grid


def relax_grid_n_times(grid, n):
	for i in range(0, n):
		grid = relax_grid(grid)
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


def spring_break_loop(grid, relax_iterations):
	relaxed_grid = relax_grid_n_times(grid, relax_iterations)
	broken_spring = max_strain_spring(relaxed_grid)
	while broken_spring is not None:
		relaxed_grid.remove_spring(broken_spring)
		relaxed_grid = relax_grid_n_times(relaxed_grid, relax_iterations)
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


def decrease_lambda_loop(grid, min_lambda, decrement_step_size, relax_iterations):
	decreased_grid = decrease_lambda(grid, decrement_step_size)
	while decreased_grid.lambda_val > min_lambda:
		print("Cur lambda= {}".format(decreased_grid.lambda_val))
		spring_snapped_grid = spring_break_loop(decreased_grid, relax_iterations)
		plot_grid(spring_snapped_grid)
		decreased_grid = decrease_lambda(spring_snapped_grid, decrement_step_size)
	return spring_snapped_grid

mu = 0.01
free_memory = True

def main():
	grid = sqaureGrid.create_sqaure_point_grid(70, 70, 69.0)
	print(grid.lambda_val)
	plot_grid(grid)
	min_lambda = 0.4
	decrement_step_size = 0.05
	relax_iterations = 5

	grid = decrease_lambda_loop(grid, min_lambda, decrement_step_size, relax_iterations)
	show_plot()

if __name__ == "__main__":
    main()




























