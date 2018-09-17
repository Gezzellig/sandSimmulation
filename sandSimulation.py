import matplotlib.pyplot as plt
import random
import math

#Currently points[0][0] is the left top element
#So it has max y and min x

class Grid:
	def __init__(self, lambda_val, points, edge_points):
		self.lambda_val = lambda_val
		self.points = points
		self.edge_points = edge_points


class Point:
	def __init__(self, position):
		self.springs = list()
		self.position = position
		self.next_point = None

	def add_spring(self, spring):
		self.springs.append(spring)

	def add_next_point(self, next_point):
		self.next_point = next_point

	def __repr__(self):
		x, y = self.position
		return "{:.2f},{:.2f} {}".format(x, y, self.next_point)

class Spring:
	def __init__(self, springconstant, strain_threshold, point1, point2):
		self.springconstant = springconstant
		self.strain_threshold = strain_threshold
		self.point1 = point1
		point1.add_spring(self)
		self.point2 = point2
		point2.add_spring(self)
		
	def __repr__(self):
		return "{}, {}, {}:{}".format(self.springconstant, self.strain_threshold, self.point1, self.point2)


def calc_position(h, w, height, width, field_size):
	offset_x = 0.1
	offset_y = 0.1
	y_pos = (field_size/(height-1))*(height-(h+1)) + random.uniform(-offset_y, offset_y)
	x_pos = (field_size/(width-1))*(w) + random.uniform(-offset_x, offset_x)
	return x_pos, y_pos


def create_points(height, width, field_size):
	points = list()
	for h in range(0, height):
		points.append(list())
		for w in range(0, width):
			points[h].append(Point(calc_position(h, w, height, width, field_size)))
	return points


def out_bounds(h, w, height, width):
	return h < 0 or w < 0 or h >= height or w >= width 


def create_spring_with_check(h, w, height, width, point, points_grid):
	springconstant = 1.0
	strain_threshold = 1.0
	if not out_bounds(h, w, height, width):
		Spring(springconstant, strain_threshold, point, points_grid[h][w])


def link_points(height, width, points_grid):
	for h in range(0, height):
		for w in range(0, width):
			point = points_grid[h][w]
			create_spring_with_check(h+1, w, height, width, point, points_grid)
			create_spring_with_check(h, w+1, height, width, point, points_grid)


def create_sqaure_point_grid(height, width, field_size):
	if not height == width:
		error("height should be equal to width")
	start_lambda = field_size / (height - 1)
	
	points_grid = create_points(height, width, field_size)
	link_points(height, width, points_grid)
	points = list()
	for h in range(1, len(points_grid)-1):
		for w in range(1, len(points_grid[h])-1):
			points.append(points_grid[h][w])
			
	edge_points = list()
	for h in range(1, len(points_grid)-1):
		edge_points.append(points_grid[h][0])
		edge_points.append(points_grid[h][-1])
	for w in range(1, len(points_grid[0])-1):
		edge_points.append(points_grid[0][w])
		edge_points.append(points_grid[-1][w])
	return Grid(start_lambda, points, edge_points)

"""
def calc_hex_position(h, w, height, width, even_row):
	field_size = 1.0
	offset_x = 0.01
	offset_y = 0.01
	y_pos = (field_size/(height+1))*(height-(h))# + random.uniform(-offset_y, offset_y)
	if even_row:
		w += 0.25
	else:
		w -= 0.25
	x_pos = (field_size/(width+1))*(w+1)# + random.uniform(-offset_x, offset_x)
	return (y_pos, x_pos)

def create_hex_grid_points(height, width):
	points = list()
	for h in range(0, height):
		points.append(list())
		for w in range(0, width):
			points[h].append(Point(calc_hex_position(h, w, height, width, h%2 == 0)))
	return points


def link_points_hex(height, width, points):
	for h in range(0, height):
		for w in range(0, width):
			#MODIFY THIS STILLLLL
			point = points[h][w]
			create_spring_with_check(h+1, w, height, width, point, points)
			create_spring_with_check(h, w+1, height, width, point, points)
			create_spring_with_check(h, w+1, height, width, point, points)


def create_hex_point_grid():
	height = 10
	width = 10
	points = create_hex_grid_points(height, width)
	#link_points_hex(height, width, points)
	return points
"""

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


def get_unique_springs(grid):
	unique_springs = set()
	for point in grid.points:
		for spring in point.springs:
			unique_springs.add(spring)
	return unique_springs


def plot_springs(grid):
	for spring in get_unique_springs(grid):
		plot_spring(spring)


def plot_forces(grid):
	for point in grid.points:
		x, y = point.position
		force_x, force_y = calc_force(point, grid.lambda_val)
		plt.arrow(x, y, force_x, force_y)


def plot_points(grid):
	points = grid.points
	edge_points = grid.edge_points
	xs, ys = get_xs_ys(points)
	plt.scatter(xs, ys, color="r", zorder=2)
	xs, ys = get_xs_ys(edge_points)
	plt.scatter(xs, ys, color="b", zorder=2)


def plot_grid(grid):
	plt.figure()
	plot_points(grid)
	plot_springs(grid)
	plot_forces(grid)


springconstant = 1.0
#friction_threshold = 0.9
#number of relaxation after is spring is broken = 20
#breaking treshold is gaussian distributed.


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
	x, y = point.position
	relaxed_position = (x + (move_x*0.1), y + move_y*0.1)
	relaxed_point = Point(relaxed_position)
	point.add_next_point(relaxed_point)
	return relaxed_point


def reconnect_grid(grid):
	for spring in get_unique_springs(grid):
		point1 = spring.point1.next_point
		point2 = spring.point2.next_point
		Spring(spring.springconstant, spring.strain_threshold, point1, point2)
			

def relax_grid(grid):
	lambda_val = grid.lambda_val
	relaxed_grid = Grid(lambda_val, list(), list())
	for edge_point in grid.edge_points:
		new_edge_point = Point(edge_point.position)
		edge_point.add_next_point(new_edge_point)
		relaxed_grid.edge_points.append(new_edge_point)
	for point in grid.points:
		relaxed_grid.points.append(relax_point(point, lambda_val))
	reconnect_grid(grid)
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
	for spring in get_unique_springs(grid):
		rel_strain = calc_strain(spring, grid.lambda_val) - spring.strain_threshold
		if rel_strain > max_rel_strain:
			max_rel_strain = rel_strain
			max_rel_strain_spring = spring
	return max_rel_strain_spring


def remove_spring(spring):
	spring.point1.springs.remove(spring)
	spring.point2.springs.remove(spring)


def spring_break_loop(grid, relax_iterations):
	relaxed_grid = relax_grid_n_times(grid, relax_iterations)
	broken_spring = max_strain_spring(relaxed_grid)
	while broken_spring is not None:
		remove_spring(broken_spring)
		relaxed_grid = relax_grid_n_times(relaxed_grid, relax_iterations)
		broken_spring = max_strain_spring(relaxed_grid)
	return relaxed_grid


def decrease_lambda(grid, decrement_step_size):
	lambda_val = grid.lambda_val - decrement_step_size
	decreased_grid = Grid(lambda_val, list(), list())
	for edge_point in grid.edge_points:
		new_edge_point = Point(edge_point.position)
		edge_point.add_next_point(new_edge_point)
		decreased_grid.edge_points.append(new_edge_point)
	for point in grid.points:
		new_point = Point(point.position)
		point.add_next_point(new_point)
		decreased_grid.points.append(new_point)
	reconnect_grid(grid)
	return decreased_grid


def decrease_lambda_loop(grid, min_lambda, decrement_step_size, relax_iterations):
	decreased_grid = decrease_lambda(grid, decrement_step_size)
	while decreased_grid.lambda_val > min_lambda:
		print("Cur lambda= {}".format(decreased_grid.lambda_val))
		spring_snapped_grid = spring_break_loop(decreased_grid, relax_iterations)
		plot_grid(spring_snapped_grid)
		decreased_grid = decrease_lambda(spring_snapped_grid, decrement_step_size)
	return spring_snapped_grid


def main():
	grid = create_sqaure_point_grid(30, 30, 29.0)
	print(grid.lambda_val)
	plot_grid(grid)
	min_lambda = 0.4
	decrement_step_size = 0.05
	relax_iterations = 30
	grid = decrease_lambda_loop(grid, min_lambda, decrement_step_size, relax_iterations)
	plt.show()

if __name__ == "__main__":
    main()




























