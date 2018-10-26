import numpy.random

class Grid:
	"""
	Represents the grid that is used in the simulation.
	"""
	def __init__(self, lambda_val, points, edge_points, springs):
		"""
		Initializes a grid.

		:param lambda_val: The lambda value applicable for this grid.
		:param points: The points in this grid.
		:param edge_points: The edge point in this grid.
		:param springs: The springs in this grid.
		"""
		self.lambda_val = lambda_val
		self.points = points
		self.edge_points = edge_points
		self.springs = springs


	def remove_spring(self, spring):
		"""
		Removes a spring from its list and from the both the points.

		:param spring: The spring that has to be removed.
		"""
		self.springs.remove(spring)
		spring.point1.springs.remove(spring)
		spring.point2.springs.remove(spring)


class Point:
	"""
	Represents a point in a grid, it can be connected to other points using springs.
	"""
	def __init__(self, position):
		"""
		Initializes a point. Initially not connected to any springs.

		:param position: The position of the point
		"""
		self.springs = list()
		self.position = position
		self.next_point = None

	def add_spring(self, spring):
		"""
		Adds a spring to its spring list.
		:param spring: The spring to be added.
		"""
		self.springs.append(spring)

	def add_next_point(self, next_point):
		"""
		Updates the value of next point, this allows the program te reconnect a new grid.

		:param next_point: its successor in the next grid.
		"""
		self.next_point = next_point

	def __repr__(self):
		x, y = self.position
		return "{:.2f},{:.2f} {}".format(x, y, self.next_point)

class Spring:
	"""
	Represents a spring, it connects two points together and has a springconstant and a strain threshold.
	"""
	def __init__(self, springconstant, strain_threshold, point1, point2):
		"""
		Initializes a spring.

		:param springconstant: The applicable springconstant.
		:param strain_threshold: The applicable strain threshold.
		:param point1: The first point it connects.
		:param point2: The second point it connects.
		"""
		self.springconstant = springconstant
		self.strain_threshold = strain_threshold
		self.point1 = point1
		point1.add_spring(self)
		self.point2 = point2
		point2.add_spring(self)

	def other_point(self, point):
		"""
		Selects the other point this spring connects to.
		
		:param point: The current point.
		:return: Other point.
		"""
		if self.point1 == point:
			return self.point2
		else:
			return self.point1

	def __repr__(self):
		return "{}, {}, {}:{}".format(self.springconstant, self.strain_threshold, self.point1, self.point2)

def create_new_spring(springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, point1, point2):
	"""
	Creates a spring using the given standard-deviation values.
	"""
	return Spring(numpy.random.normal(springconstant_normal,springconstant_deviation), numpy.random.normal(strain_normal, strain_deviation), point1, point2)
