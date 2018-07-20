class Node:

	parent = None
	X = 0
	Y = 0
	linkedNodes = {}

	def Node(parent, X, Y, linkedNodes):
		self.parent = parent
		self.X = X
		self.Y = Y
		self.linkedNodes = linkedNodes