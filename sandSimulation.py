import matplotlib.pyplot as plt

#Currently points[0][0] is the left top element
#So it has max y and min x

class point:
	def __init__(self, position):
		self.neighbours = list()
		self.position = position

	def add_neighbour(self, neighbour):
		self.neighbours.append(neighbour)
		

def calc_position(h, w, height, width):
	field_size = 1.0
	offset_factor = 0.1
	y_offset = offset_factor*(field_size/(height+1))
	x_offset = offset_factor*(field_size/(width+1))
	y_pos = (field_size/(height+1))*(height-(h)) 
	x_pos = (field_size/(width+1))*(w+1)
	return (y_pos, x_pos)


def create_points(height, width):
	points = list()
	for h in range(0, height):
		points.append(list())
		for w in range(0, width):
			points[h].append(point(calc_position(h, w, height, width)))
	return points


def out_bounds(h, w, height, width):
	return h < 0 or w < 0 or h >= height or w >= width 


def add_neighbour_with_check(h, w, height, width, point, points):
	if not out_bounds(h, w, height, width):
		point.add_neighbour(points[h][w])


def link_points(height, width, points):
	for h in range(0, height):
		for w in range(0, width):
			point = points[h][w]
			add_neighbour_with_check(h-1, w, height, width, point, points)
			add_neighbour_with_check(h+1, w, height, width, point, points)
			add_neighbour_with_check(h, w-1, height, width, point, points)
			add_neighbour_with_check(h, w+1, height, width, point, points)


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


def plot_lines_point(point):
	for neighbour in point.neighbours:
		point_y, point_x = point.position
		neigh_y, neigh_x = neighbour.position 
		if point_y >= neigh_y and point_x <= neigh_x:
			plt.plot([point_x, neigh_x], [point_y, neigh_y], color='k', linestyle='-', zorder=1)


def plot_lines(points):
	for row in points:
		for point in row:
			plot_lines_point(point)


def plot_points(points):
	xs, ys = get_xs_ys(points)
	plt.scatter(xs, ys, color="r", zorder=2)
	plot_lines(points)
	plt.show()


springconstant = 1.0
friction_threshold = 0.9
number of relaxation after is spring is broken = 20
breaking treshold is gaussian distributed.


def main():
	points = create_sqaure_point_grid()
	print(points[0][0].position)
	print(points[0][1].position)
	print(points[1][1].position)
	print(points[1][2].position)
	plot_points(points)

if __name__ == "__main__":
    main()




























