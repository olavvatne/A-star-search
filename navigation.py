from abstractNode import Node
from math import fabs

# Specific implementation of the abstract node class. Will handle navigation tasks.
# Customized for problem domain.
#THe specialization of the A* algorithm. Other subclasses of Node can be made for other
#problem. THe general A* implementation works either way as long as the abstract methods are implemented
# Id - the coordinate of the node
# successors - generated using the state
# H - Calculated using the manhattan distance from the current position to the goal position
# arcCost - It cost 1 moving from one node to another. 
# Minimizing the total arcCost from start to goal gives the optimal path.
#
#(NOTE: Should probably just have a node, and instead an abstract state, and a specialization of state, but this works)
class NavigationNode(Node):

	def __init__(self, state, x, y):
		super().__init__()
		self.state = state
		self.x = x
		self.y = y

	#The state containing the map,goal and start generate all successors when knowing the
	#position of the current node and the parent nodes x,y values
	def generateSuccessors(self):
		return self.state.generateSuccessors(self, self.getParent())

	#The admissable heuristic for this A-B navigation problem use manhattan distance as its heuristic.
	#The number return is the least amount of moves that is required to get from the current position on the board
	#To the goal position. The number will either be correct or too optimistic, since obstacles might be in the way,
	#resulting more moves being necessary for getting to the goal position.
	def calcH(self):
		return fabs(self.x-self.state.gx) + fabs(self.y-self.state.gy);

	#Since the A* tries to find its way from point A-B on a 2D surface, the id contains both
	#the x and y coordinate. Nodes can now be differentiated, or deemed identical.
	def generateId(self):
		#Board pos x,y
		return str(self.x) + "-"+ str(self.y)

	#The cost of moving from one node to another node is in this case 1. 
	def arcCost(self, child):
		return self.state.movementPenalty()

	#This node can be considered a solution if its x and y coordinate is equal to the goal states x and y coordinates.
	def isSolution(self):
		return self.x == self.state.gx and self.y == self.state.gy

	#The guiRepresentation for this particular problem domain. A-B navigation, construct the
	#best path from start to this current node. It returns an list of coordinate tuples, that
	#a gui can use to draw the current best path from start to current node.
	def guiRepresentation(self):
		path = []
		p = self
		while p:
			path.insert(0, (p.x, p.y))
			p = p.getParent()

		return path

	#How the node should represent itself if printed.
	def __repr__(self):
		return str(self.x) + "," + str(self.y)


#State contain the start, goal and obstacles.
class NavigationState(object):

	def __init__(self, start, goal, dimension,obstacles):
		self.width = dimension[0]
		self.height = dimension[1]
		self.gx = goal[0]
		self.gy = goal[1]
		self.sx = start[0]
		self.sy = start[1]
		self.obstacles = obstacles

		self.map = []
		for i in range(self.height):
			self.map.append([])
			for j in range(self.width):
				self.map[i].append(False)
		self.generateObstacleMap(obstacles)

	def movementPenalty(self):
		return 1

	#An obstacle map has to be generated for the generateSuccessors method to work properly.
	#It consist of a list consisting of more list. The latter represent each row for the
	#bord. In cells covered in an obstacle the map is set to True.
	def generateObstacleMap(self, obstacles):
		for x,y,w,h in obstacles:
			for j in range(y, y+h):
				for i in range(x, x+w):
					self.map[j][i] = True

	#The state know how the board looks, where the goal is and is therefore responsible for
	#generating the children for a arbitrary node. The method use the node x and y coordinate to
	#see what directions the path can take. 
	def generateSuccessors(self, node, parent):
		#The parent cell should not be both the parent and child node of 'node'
		if not parent:
			parent = NavigationNode(self, -1, -1)
		x = node.x
		y = node.y
		s = []
		if x+1 < self.width and x+1 is not parent.x and not self.map[y][x+1]:
			s.append(NavigationNode(self, x+1, y)) 
		if x-1 >= 0 and x-1 is not parent.x and not self.map[y][x-1]:
			s.append(NavigationNode(self, x-1, y))
		if y-1 >= 0 and y-1 is not parent.y and not self.map[y-1][x]:
			s.append(NavigationNode(self, x, y-1))
		if y+1 < self.height and y+1 is not parent.y and not self.map[y+1][x]:
			s.append(NavigationNode(self, x, y+1))
		return s


