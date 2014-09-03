from tkinter import *
from tkinter import ttk
from enum import Enum
import math
from collections import deque

##Canvas gui component. The board is drawn onto this canvas. PixelDisplay contain
#method for drawing obstacles, goal, start, and setting dimensions. 
class PixelDisplay(Canvas):
	cWi = 500
	cHi = 300
	pixelSize = 10

	def __init__(self, parent):
		self.padding = 20
		self.queue = deque([])
		super().__init__(parent, bg='white', width=self.cWi, height=self.cHi)

	def setModel(self, model):
		if not hasattr(model, "obstacles"):
			raise Exception("No list of obstacles")
		#TODO better way interface?
		self.model = model

	#Draw loop. WHen pixelDisplay is started the draw method is called. As long as
	#the display is not stopped or there are snapshots in the gui buffer, the draw
	#is in a loop. Each time, the board is reset, dimensions set, and obstacles and
	# the current best path drawn.
	def draw(self):
		self.reset()
		self.setDimension( self.model.width, self.model.height )

		if len(self.queue)>0:
			timeSlice = self.queue.popleft()
			currentPath = timeSlice[0]
			generated = timeSlice[1]
			isSolution = timeSlice[2]
			pathLength = len(currentPath) -1
			for x, y in currentPath:
				self.drawPixel(x, y, FillColor.PATH)

			self.drawStart( self.model.sx, self.model.sy, FillColor.START )
			self.drawEnd( self.model.gx, self.model.gy, FillColor.GOAL )
			for x,y,w,h in self.model.obstacles:
				self.drawObstacle( x, y, w, h )
			self.create_text(400, 20, text=("Generated: " + str(generated)))
			self.create_text(400, 40, text=("Best path: " + str(pathLength)))
			if isSolution:
				self.create_text(400, 60, text=("A solution!"))
			else:
				self.create_text(400, 60, text=("Not a solution!"))


		if not self.stopped or len(self.queue) > 0:
			self.after(100, self.draw)


	def start(self):
		self.stopped = False
		self.draw()

	def stop(self):
		self.stopped = True

	#The actual position of a board cell/pixel.
	def gridPos(self, pos):
		return self.padding+ (pos*self.pixelSize)

	def reset(self):
		self.delete(ALL)

	#By setting the dimension the pixelSize is determined.
	#Based on the width and height the board is scaled to fit inside the canvas.
	def setDimension(self, width, height):
		self.reset()
		self.width = width
		self.height = height
		if height >= width:
			self.pixelSize = math.floor((self.cHi-2*self.padding) / height)
		else:
			self.pixelSize = math.floor( (self.cWi-2*self.padding) / width)
		self.create_rectangle(self.padding, self.padding,
							  self.padding + width*self.pixelSize,
							  self.padding + height*self.pixelSize,
							  fill="white")

	def setPadding(self, padding):
		self.padding = padding

	#Event listener method. For the object to be accepted as a listener it has to have
	#this method, or else an exception is raised.
	def event(self, node, generated, solution):
		self.queue.append((node.guiRepresentation(), generated, solution))

	#draws a cell.
	def drawPixel(self, x,y, c):
		x = self.gridPos(x)
		y = self.gridPos(y)
		self.create_rectangle(x, y, x+self.pixelSize, y+self.pixelSize, fill=c.value)
	
	#draws the start cell
	def drawStart(self, x,y,c):
		self.drawPixel(x,y,c)
		x = self.gridPos(x)
		y = self.gridPos(y)
		self.create_text(x+ self.pixelSize*1/2,y + self.pixelSize*1/2, text="S")

	#draws the goal cell
	def drawEnd(self, x,y,c):
		self.drawPixel(x,y,c)
		x = self.gridPos(x)
		y = self.gridPos(y)
		self.create_text(x + self.pixelSize*1/2, y + self.pixelSize*1/2, text="E")

	#Draws a red rectangle representing an obstacle
	def drawObstacle(self, x, y, w, h):
		x = self.gridPos(x)
		y = self.gridPos(y)
		self.create_rectangle(x,
							y,
							x+self.pixelSize*w,
							y+self.pixelSize*h,
							fill=FillColor.OBSTACLE.value)

#Enum for fill colors for the different cells in the canvas.
class FillColor(Enum):
	PATH = "blue"
	OBSTACLE = "red"
	GOAL = "grey"
	START = "grey"
	NONE = "white"
