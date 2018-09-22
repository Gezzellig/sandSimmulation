import random
import math
from classes import Grid, Point, Spring, create_new_spring

def calc_position(h, w, height, width, field_size):
	offset_x = 0.1
	offset_y = 0.1
	rx = random.uniform(-offset_x, offset_x)
	ry = random.uniform(-offset_y, offset_y)

	dx = field_size/(width-1)
	# Property of equilateral triangle: height = sqrt(3)/2 * (length_of_side)
	dy = 0.5 * math.sqrt(3) * dx

	x_pos = w*dx + (0.5*dx if h % 2 == 0 else 0)
	y_pos = (height - (h+1))*dy

	return x_pos + rx, y_pos + ry


def create_points(height, width, field_size):

	def last_in_even_row(w, h):
		return w == width-1 and h % 2 == 0
	
	def surplus_edges_in_first_row(w, h):
		return h == height-1 and (w == 0 or w == width-1)

	return [[Point(calc_position(h, w, height, width, field_size)) for w in range(0, width) if not last_in_even_row(w,h) ] for h in range(0, height)]


def link_points(height, width, strain_normal, strain_deviation, points_grid):
	def spr(a, b):
		return create_new_spring(1.0, strain_normal, strain_deviation, a, b)
		
	springs = []
	# Diagonal springs
	for h in range(0, height-1):
		springs += [ spr(a,b) for a,b in zip(points_grid[h][1:], points_grid[h+1][1:])]
		offset = 1 if h % 2 == 0 else 0
		springs += [ spr(a,b) for a,b in zip(points_grid[h][(1-offset):-1], points_grid[h+1][offset:])]
			
	# Horizontal springs
	for h in range(1, height-1):
		springs += [ spr(a,b) for a,b in zip(points_grid[h][:-1], points_grid[h][1:])]
	
	return springs


def create_hex_point_grid(height, width, field_size, strain_normal, strain_deviation):
	start_lambda = field_size / (height - 1)
	
	points_grid = create_points(height, width, field_size)
	springs = link_points(height, width, strain_normal, strain_deviation, points_grid)

	points = []
	for h in range(1, len(points_grid)-1):
		points += [points_grid[h][w] for w in range(1, len(points_grid[h])-1)]

	edge_points = points_grid[0] + points_grid[-1] + [ points_grid[h][w] for h in range(1, len(points_grid)-1) for w in [0, -1]]

	return Grid(start_lambda, points, edge_points, springs)
