import matplotlib.pyplot as plt
import random

#Currently points[0][0] is the left top element
#So it has max y and min x

class Point:
	def __init__(self, position):
		self.springs = list()
		self.position = position

	def add_spring(self, spring):
		self.springs.append(spring)


class Spring:
	def __init__(self, springconstant, breakforce, point1, point2):
		self.springconstant = springconstant
		self.breakforce = breakforce
		self.point1 = point1
		point1.add_spring(self)
		self.point2 = point2
		point2.add_spring(self)


def calc_position(h, w, height, width):
	field_size = 1.0
	offset_x = 0.01
	offset_y = 0.01
	y_pos = (field_size/(height+1))*(height-(h)) + random.uniform(-offset_y, offset_y)
	x_pos = (field_size/(width+1))*(w+1) + random.uniform(-offset_x, offset_x)
	return (y_pos, x_pos)


def create_points(height, width):
	points = list()
	for h in range(0, height):
		points.append(list())
		for w in range(0, width):
			points[h].append(Point(calc_position(h, w, height, width)))
	return points


def out_bounds(h, w, height, width):
	return h < 0 or w < 0 or h >= height or w >= width 


def create_spring_with_check(h, w, height, width, point, points):
	springconstant = 1.0
	breakforce = 1.0
	if not out_bounds(h, w, height, width):
		Spring(springconstant, breakforce, point, points[h][w])


def link_points(height, width, points):
	for h in range(0, height):
		for w in range(0, width):
			point = points[h][w]
			create_spring_with_check(h+1, w, height, width, point, points)
			create_spring_with_check(h, w+1, height, width, point, points)


def create_sqaure_point_grid():
	height = 10
	width = 10
	points = create_points(height, width)
	link_points(height, width, points)
	return points


def get_xs_ys(points):
	xs = list()
	ys = list()
	for row in points:
		for point in row:
			y, x = point.position
			xs.append(x)
			ys.append(y)
	return xs, ys


def plot_spring(spring):
	point1_y, point1_x = spring.point1.position
	point2_y, point2_x = spring.point2.position 
	plt.plot([point1_x, point2_x], [point1_y, point2_y], color='k', linestyle='-', zorder=1)


def plot_springs(points):
	unique_springs = set()
	for row in points:
		for point in row:
			for spring in point.springs:
				unique_springs.add(spring)
	for spring in unique_springs:
		plot_spring(spring)


def plot_points(points):
	xs, ys = get_xs_ys(points)
	plt.scatter(xs, ys, color="r", zorder=2)
	plot_springs(points)
	plt.show()


#springconstant = 1.0
#friction_threshold = 0.9
#number of relaxation after is spring is broken = 20
#breaking treshold is gaussian distributed.


def main():
	points = create_sqaure_point_grid()
	plot_points(points)

if __name__ == "__main__":
    main()




























