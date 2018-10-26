import random
from classes import Grid, Point, Spring, create_new_spring

def calc_position(h, w, dim):
	"""
	Calculate the position of a point on a square grid with a random offset.

	:param h: height point coordinate.
	:param w: width point coordinate.
	:param dim: The size of the grid.
	:return: 2d vector containing the position.
	"""
	offset_x = 0.1
	offset_y = 0.1
	dx = 1
	dy = 1
	y_pos = dy*(dim-(h+1)) + random.uniform(-offset_y, offset_y)
	x_pos = dx*w + random.uniform(-offset_x, offset_x)

	return x_pos, y_pos


def create_points(dim):
	"""
	Creates all the points with their appropriate locations for a square grid.

	:param dim: The size of the grid
	:return: List of points.
	"""
	points = list()
	for h in range(0, dim):
		points.append(list())
		for w in range(0, dim):
			points[h].append(Point(calc_position(h, w, dim)))
	return points


def out_bounds(h, w, dim):
	"""
	Checks if the point requested is not out of bounds
	"""
	return h < 0 or w < 0 or h >= dim or w >= dim 


def create_spring_with_check(h, w, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, point, points_grid):
	"""
	Uses an out of bounds check to create the spring between the given point and a point given by location h and w

	:param h: height location of the other point
	:param w: width location of the other point
	:param dim: The size of the grid
	:param springconstant_normal: The normal of the springconstant.
	:param springconstant_deviation: The deviation of the springconstant on this normal.
	:param strain_normal: The normal of the strain.
	:param strain_deviation: The deviation of the strain on this normal.
	:param point: The given point
	:param points_grid: The grid containing all the points.
	:return: The spring that is created.
	"""
	if not out_bounds(h, w, dim):
		return create_new_spring(springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, point, points_grid[h][w])


def link_points(dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, points_grid):
	"""
	Link all the points in a square grid manner.
	:param dim: The size of the grid
	:param springconstant_normal: The normal of the springconstant.
	:param springconstant_deviation: The deviation of the springconstant on this normal.
	:param strain_normal: The normal of the strain.
	:param strain_deviation: The deviation of the strain on this normal.
	:param points_grid: The grid containing all the points.
	:return:
	"""
	springs = list()
	for h in range(1, dim-1):
		point = points_grid[h][0]
		spring = create_spring_with_check(h, 1, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, point, points_grid)
		if not spring is None:
			springs.append(spring)
			
	for w in range(1, dim-1):
		point = points_grid[0][w]
		spring = create_spring_with_check(1, w, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, point, points_grid)
		if not spring is None:
			springs.append(spring)
	
	
	for h in range(1, dim-1):
		for w in range(1, dim-1):
			point = points_grid[h][w]
			spring = create_spring_with_check(h+1, w, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, point, points_grid)
			if not spring is None:
				springs.append(spring)
			spring = create_spring_with_check(h, w+1, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, point, points_grid)
			if not spring is None:
				springs.append(spring)
	return springs


def create_square_grid(dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation):
	"""
	Creates a square grid using the given size and values applicable for the springs.

	:param dim: The size of the grid
	:param springconstant_normal: The normal of the springconstant.
	:param springconstant_deviation: The deviation of the springconstant on this normal.
	:param strain_normal: The normal of the strain.
	:param strain_deviation: The deviation of the strain on this normal.
	:return:
	"""
	start_lambda = 1
	
	points_grid = create_points(dim)
	springs = link_points(dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, points_grid)
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
	return Grid(start_lambda, points, edge_points, springs)
