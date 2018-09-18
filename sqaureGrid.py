import random
from classes import Grid, Point, Spring

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
		return Spring(springconstant, strain_threshold, point, points_grid[h][w])


def link_points(height, width, points_grid):
	springs = list()
	for h in range(1, height-1):
		point = points_grid[h][0]
		spring = create_spring_with_check(h, 1, height, width, point, points_grid)
		if not spring is None:
			springs.append(spring)
			
	for w in range(1, width-1):
		point = points_grid[0][w]
		spring = create_spring_with_check(1, w, height, width, point, points_grid)
		if not spring is None:
			springs.append(spring)
	
	
	for h in range(1, height-1):
		for w in range(1, width-1):
			point = points_grid[h][w]
			spring = create_spring_with_check(h+1, w, height, width, point, points_grid)
			if not spring is None:
				springs.append(spring)
			spring = create_spring_with_check(h, w+1, height, width, point, points_grid)
			if not spring is None:
				springs.append(spring)
	return springs


def create_sqaure_point_grid(height, width, field_size):
	if not height == width:
		error("height should be equal to width")
	start_lambda = field_size / (height - 1)
	
	points_grid = create_points(height, width, field_size)
	springs = link_points(height, width, points_grid)
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