import os
import maze
from PIL import Image
import random
import time

building = []
mappedBuilding = []
visitedJunctions = []

def saveMazeImage(building):

	imgx = 500; imgy = 500
	color = [(0, 0, 0), (255, 255, 255), (250,0,0), (0,255,0)] # RGB colors of the maze

	image = Image.new("RGB", (imgx, imgy))
	pixels = image.load()

	for ky in range(imgy):
	    for kx in range(imgx):
	        pixels[kx, ky] = color[building[building.shape[1]*ky/imgy, building.shape[0]*kx/imgx]]
	image.save("MappedMaze.png", "PNG")


def getOpenNeighbours(x, y, maze, prev):

	openNodes = []
	directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

	for d in directions:
		nextX = x + d[0]
		nextY = y + d[1]
		if maze[nextX][nextY]==1:
			openNodes.append(((nextX,nextY),d))

	if len(openNodes)>1 and openNodes[0]==prev:
		return []
	
	return openNodes


#Recursive algorithm to explore maze
def exploreMap(x, y, maze, prev):

	global visitedJunctions

	visitedJunctions.append((x,y))
	
	potentialNodes = []
	openNodes = getOpenNeighbours(x, y, maze, prev)

	if len(openNodes)>0:
		 mappedBuilding[x][y] = 3

	for node in openNodes:
		if node != prev:
			potentialNodes.append(node)

	while len(potentialNodes)>0:

		nextNode, direction = potentialNodes.pop(0)

		currX, currY = nextNode[0], nextNode[1]
		while maze[currX][currY]==1:
			mappedBuilding[currX][currY]=2
			
			saveMazeImage(mappedBuilding)

			if len(getOpenNeighbours(currX, currY, maze, prev))>=2:
				previous = (currX-direction[0], currY-direction[1])
				exploreMap(currX, currY, maze, previous)

			currX += direction[0]
			currY += direction[1]

		currX -= direction[0]
		currY -= direction[1]

		previous = (currX-direction[0], currY-direction[1])
		exploreMap(currX, currY, maze, previous)


dim = 15
robot_number = 1

building = maze.generateMaze(dim, dim, robot_number)
mappedBuilding = building

random.seed(time.time())

os.system('xdg-open ./MappedMaze.png')
exploreMap(1, 1, building, (1,1))

saveMazeImage(mappedBuilding)

#print building
