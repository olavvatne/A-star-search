from abc import ABCMeta, abstractmethod

#Node object, important for traversing the search graph. Abstract class
#that contain abstract methods that has to be implemented by subclasses.
#These abstract methods, is what constitute the specialization of the A*
#for this problem domain.
class Node(object):
	__metaclass__ = ABCMeta

	def __init__(self):
		self.children = []
		self.parents = []

	#Generate successor nodes/states from itself.
	@abstractmethod
	def generateSuccessors(self):
		pass

	#A getter for the heuristic. The heuristic is the estimate of the nearness to
	#the goal the specific node is. In case of a distance A to B problem, 
	#the H is the admissable (no overestimates) distance from the goal from the nodes position.
	@abstractmethod
	def calcH(self):
		pass

	#The actual distance from start to the node. The path cost.
	def getG(self):
		return self.g

	def setG(self, cost):
		self.g = cost

	#Each node has to have to generate a id, to assess the uniqueness of the node. 
	@abstractmethod
	def generateId(self):
		pass

	#ArcCost from self to children. The pathcost from one node to another
	@abstractmethod
	def arcCost(self, child):
		pass

	#If node is a solution
	@abstractmethod
	def isSolution(self):
		pass

	def addChild(self, node):
		self.children.append(node)

	def setParent(self, node):
		#TODO: ONE PARENT?
		self.parents = []
		self.parents.append(node)

	def getChildren(self):
		return self.children

	def getParent(self):
		#TODO: ONE PARENT?
		if not self.parents:
			return None

		return self.parents[0]

	def calcF(self):
		return self.getG() + self.calcH()

	def __lt__(self, other):
		return self.calcF() < other.calcF()

	#Representation for the GUI
	@abstractmethod
	def guiRepresentation(self):
		pass
