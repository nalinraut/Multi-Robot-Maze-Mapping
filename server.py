import select
import socket
import sys
import maze
import json
from PIL import Image

numRobots = 4

mazeDim = int(sys.argv[2])
building = maze.generateMaze(mazeDim, mazeDim)
globalMappedBuilding = building

serverSocket = None
closeCalls = []
exitedClients = []

step = 0

def saveGlobalMazeImage(building, step):

	imgx = 400; imgy = 400
	color = [(255, 255, 255), (0, 0, 0), (250,0,0), (0,255,0)] # RGB colors of the maze

	image = Image.new("RGB", (imgx, imgy))
	pixels = image.load()

	for ky in range(imgy):
	    for kx in range(imgx):
	        pixels[kx, ky] = color[building[len(building)*ky/imgy][len(building[0])*kx/imgx]]
	image.save("Global/"+str(step)+".png", "PNG")


def createServerSocket(port):

	global serverSocket

	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', port)
	serverSocket.bind(server_address)

	serverSocket.listen(5)

def synchronizeWithClients():

	global serverSocket, globalMappedBuilding
	global step

	inputs = []
	outputs = []
	errs = []

	while len(inputs)<numRobots:
		conn, clientAddr = serverSocket.accept()
		conn.setblocking(0)
		inputs.append(conn)
		outputs.append(conn)

	for conn in inputs:

		buildingString = json.dumps(building)
		conn.send(buildingString)

	while True:

		readable, writable, erronous = select.select(inputs, outputs, errs)

		while len(readable)<numRobots:
			readable, writable, erronous = select.select(inputs, outputs, errs)
			pass

		for sock in readable:

			mappedBuildingString = []
			mappedBuildingString = sock.recv(1000000000)

			if mappedBuildingString=='END':
				closeCalls.append(1)
				
			elif mappedBuildingString:
				localMappedBuilding = json.loads(mappedBuildingString)
				
				for i in range(len(globalMappedBuilding)):
					for j in range(len(globalMappedBuilding[0])):

						if globalMappedBuilding[i][j]==0:
							globalMappedBuilding[i][j] ^= localMappedBuilding[i][j]

				saveGlobalMazeImage(globalMappedBuilding, step)
				step += 1

		for sock in writable:

			buildingString = json.dumps(globalMappedBuilding)
			sock.send(buildingString)


		if len(closeCalls)==numRobots:
			print "EXITINGGGGGGGGGGGGG"
			saveGlobalMazeImage(globalMappedBuilding)

			for sock in writable:
				sock.send('COMPLETE')

			#serverSocket.close()
			break


createServerSocket(int(sys.argv[1]))
synchronizeWithClients()

saveGlobalMazeImage(globalMappedBuilding, step)
serverSocket.close()