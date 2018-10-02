import matplotlib.pyplot as plt
import matplotlib.collections as mat_col
from classes import Grid, Point, Spring

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


def plot_triangles(ax, grid):
	patches = list()
	pointlist = [grid.points[36]]
	for point in grid.points:
		coordinates = list()
		for spring in point.springs:
			point_x, point_y = spring.other_point(point).position
			coordinates.append([point_x, point_y])
		if len(coordinates) > 1:
			polygon = plt.Polygon(coordinates, True)
			patches.append(polygon)
	ax.add_collection(mat_col.PatchCollection(patches))



def plot_grid(grid):
	fig, ax = plt.subplots()
	#plot_points(grid)
	#plot_springs(grid)
	plot_triangles(ax, grid)
	plot_edge_points(grid)
	#plot_forces(grid)
	
def show_plot():
	plt.show()
