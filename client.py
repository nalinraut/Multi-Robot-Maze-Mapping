import socket
import sys
import json
from PIL import Image
import os
import time
import random

building = []
mappedBuilding = []
globalBuilding = []
visitedJunctions = []

client = None

cost = 1

def saveMazeImage(building, robot_number,i):

	imgx = 400; imgy = 400

	if robot_number==1:
		color = [(255, 255, 255), (0, 0, 0), (255,0,0), (0,255,0)] # RGB colors of the maze
	elif robot_number==2:
		color = [(255, 255, 255), (0, 0, 0), (255,193,37), (0,255,0)] # RGB colors of the maze
	elif robot_number==3:
		color = [(255, 255, 255), (0, 0, 0), (255,97,3), (0,255,0)] # RGB colors of the maze
	elif robot_number==4:
		color = [(255, 255, 255), (0, 0, 0), (39,64,139), (0,255,0)] # RGB colors of the maze

	image = Image.new("RGB", (imgx, imgy))
	pixels = image.load()

	for ky in range(imgy):
	    for kx in range(imgx):
			pixels[kx, ky] = color[building[len(building)*ky/imgy][len(building[0])*kx/imgx]]
	image.save("Robot"+str(robot_number)+"/"+str(i)+".png", "PNG")


def getOpenNeighbours(x, y, maze, prev):

	openNodes = []
	directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
	random.shuffle(directions)

	for d in directions:
		nextX = x + d[0]
		nextY = y + d[1]
		if maze[nextX][nextY]==0:
			openNodes.append(((nextX,nextY),d))

	if len(openNodes)==1 and openNodes[0][0]==prev:
		return []
	
	return openNodes


#Recursive algorithm to explore maze
def exploreMap(x, y, maze, prev, robot_number):

	global mappedBuilding, globalBuilding
	global client, cost

	visitedJunctions.append((x,y))
	
	potentialNodes = []
	openNodes = getOpenNeighbours(x, y, maze, prev)

	if len(openNodes)>0:
		mappedBuilding[x][y] = 3
	
	mappedBuildingString = []
	mappedBuildingString = json.dumps(mappedBuilding)
	client.send(mappedBuildingString)

	data = client.recv(1000000000)
	if data:
		globalBuilding = json.loads(data)
	
	for node in openNodes:
		if node[0] != prev:
			potentialNodes.append(node)

	while len(potentialNodes)>0:

		currNode, direction = potentialNodes.pop(0)

		currX, currY = currNode[0], currNode[1]
		while globalBuilding[currX][currY]==0:
			
			cost+=1

			mappedBuildingString = []
			mappedBuildingString = json.dumps(mappedBuilding)
			client.send(mappedBuildingString)

			data = client.recv(1000000000)
			if data:
				globalBuilding = json.loads(data)

			saveMazeImage(mappedBuilding, robot_number,cost)

			nodeFlag = False
			if len(getOpenNeighbours(currX, currY, maze, prev))>=2 and globalBuilding[currX][currY]==0:
				nodeFlag = True
				previous = (currX-direction[0], currY-direction[1])
				exploreMap(currX, currY, maze, previous, robot_number)

			mappedBuilding[currX][currY]=2
			if nodeFlag:
				mappedBuilding[currX][currY]=3

			currX += direction[0]
			currY += direction[1]

		flag = True
		if globalBuilding[currX][currY]==2 or globalBuilding[currX][currY]==3:
			flag=False

		currX -= direction[0]
		currY -= direction[1]

		if flag:
			previous = (currX-direction[0], currY-direction[1])
			exploreMap(currX, currY, maze, previous, robot_number)


def main():

	global mappedBuilding, globalBuilding
	global client

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_addr = ('localhost', int(sys.argv[2]))
	client.connect(server_addr)

	robot_number = int(sys.argv[1])

	data = client.recv(1000000000)
	building = json.loads(data)
	mappedBuilding, globalBuilding = building, building

	saveMazeImage(mappedBuilding, robot_number,cost)
	imageOpenCommand = 'xdg-open ./MappedMaze_'+str(robot_number)+'.png'
	#os.system(imageOpenCommand)

	mazeDim = int(sys.argv[3])

	if robot_number==1:
		exploreMap(1, 1, mappedBuilding, (1,1), robot_number)
	elif robot_number==2:
		exploreMap(1, mazeDim, mappedBuilding, (1,mazeDim), robot_number)
	elif robot_number==3:
		exploreMap(mazeDim, 1, mappedBuilding, (mazeDim,1), robot_number)
	elif robot_number==4:
		exploreMap(mazeDim, mazeDim, mappedBuilding, (mazeDim,mazeDim), robot_number)

	saveMazeImage(mappedBuilding, robot_number,cost)

	print "Cost for robot",robot_number,":",2*cost

	client.send('END')

	print "EXITTT"

	postExplorationString = []
	while postExplorationString!='COMPLETE':
		
		postExplorationString = client.recv(1000000000)
		if postExplorationString:
			globalBuilding = json.loads(postExplorationString)

		mappedBuildingString = json.dumps(mappedBuilding)
		client.send(mappedBuildingString)


	print "COMPLETED"

	client.close()

main()