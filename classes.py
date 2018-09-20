import numpy.random

class Grid:
	def __init__(self, lambda_val, points, edge_points, springs):
		self.lambda_val = lambda_val
		self.points = points
		self.edge_points = edge_points
		self.springs = springs


	def remove_spring(self, spring):
		self.springs.remove(spring)
		spring.point1.springs.remove(spring)
		spring.point2.springs.remove(spring)


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

def create_new_spring(springconstant, strain_normal, strain_deviation, point1, point2):
	return Spring(springconstant, numpy.random.normal(strain_normal, strain_deviation), point1, point2)
