import random
from classes import Grid, Point, Spring, create_new_spring

def calc_position(h, w, dim):
	offset_x = 0.1
	offset_y = 0.1
	dx = 1
	dy = 1
	y_pos = dy*(dim-(h+1)) + random.uniform(-offset_y, offset_y)
	x_pos = dx*w + random.uniform(-offset_x, offset_x)

	return x_pos, y_pos


def create_points(dim):
	points = list()
	for h in range(0, dim):
		points.append(list())
		for w in range(0, dim):
			points[h].append(Point(calc_position(h, w, dim)))
	return points


def out_bounds(h, w, dim):
	return h < 0 or w < 0 or h >= dim or w >= dim 


def create_spring_with_check(h, w, dim, strain_normal, strain_deviation, point, points_grid):
	springconstant = 1.0
	if not out_bounds(h, w, dim):
		return create_new_spring(springconstant, strain_normal, strain_deviation, point, points_grid[h][w])


def link_points(dim, strain_normal, strain_deviation, points_grid):
	springs = list()
	for h in range(1, dim-1):
		point = points_grid[h][0]
		spring = create_spring_with_check(h, 1, dim, strain_normal, strain_deviation, point, points_grid)
		if not spring is None:
			springs.append(spring)
			
	for w in range(1, dim-1):
		point = points_grid[0][w]
		spring = create_spring_with_check(1, w, dim, strain_normal, strain_deviation, point, points_grid)
		if not spring is None:
			springs.append(spring)
	
	
	for h in range(1, dim-1):
		for w in range(1, dim-1):
			point = points_grid[h][w]
			spring = create_spring_with_check(h+1, w, dim, strain_normal, strain_deviation, point, points_grid)
			if not spring is None:
				springs.append(spring)
			spring = create_spring_with_check(h, w+1, dim, strain_normal, strain_deviation, point, points_grid)
			if not spring is None:
				springs.append(spring)
	return springs


def create_square_grid(dim, strain_normal, strain_deviation):
	# width = dim
	# height = dim
	# field_size = dim - 1.0

	# start lambda was field_size / (height - 1), which amounts to 1 if field_size is fixed
	start_lambda = 1
	
	points_grid = create_points(dim)
	springs = link_points(dim, strain_normal, strain_deviation, points_grid)
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
