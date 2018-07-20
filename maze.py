import os
import random
from PIL import Image
import numpy as np
import time

def isAllowed(m, x, y):

	if (m[x-1][y] & m[x-1][y+1] & m[x][y+1] == 1) or \
	   (m[x+1][y] & m[x+1][y+1] & m[x][y+1] == 1) or \
	   (m[x-1][y] & m[x-1][y-1] & m[x][y-1] == 1) or \
	   (m[x+1][y] & m[x+1][y-1] & m[x][y-1] == 1):
	   	return 0
	else:
		if (m[x-1][y] & m[x+1][y] == 1) or (m[x][y-1] & m[x][y+1] == 1):
			return 1
		else:
			return 0


def openRandomPassage(final_maze, xLower, xUpper, yLower, yUpper):

	exit = False
	while exit==False:

		randomX = random.randint(xLower, xUpper)
		randomY = random.randint(yLower, yUpper)

		if isAllowed(final_maze, randomX, randomY)==1 and final_maze[randomX][randomY]==0:
			final_maze[randomX][randomY]=1
			exit = True


def generateMaze(dimX,dimY):

	random.seed(time.time())

	imgx = 400; imgy = 400
	image = Image.new("RGB", (imgx, imgy))
	pixels = image.load()

	 # width and height of the maze
	maze = [[0 for x in range(dimX)] for y in range(dimY)]
	dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze
	color = [(255, 255, 255), (0, 0, 0)] # RGB colors of the maze

	# start the maze from a random cell
	cx = random.randint(0, dimX - 1); cy = random.randint(0, dimY - 1)
	maze[cy][cx] = 1; stack = [(cx, cy, 0)] # stack element: (x, y, direction)

	while len(stack) > 0:
	    (cx, cy, cd) = stack[-1]
	    # to prevent zigzags:
	    # if changed direction in the last move then cannot change again
	    if len(stack) > 2:
	        if cd != stack[-2][2]: dirRange = [cd]
	        else: dirRange = range(4)
	    else: dirRange = range(4)

	    # find a new cell to add
	    nlst = [] # list of available neighbors
	    for i in dirRange:
	        nx = cx + dx[i]; ny = cy + dy[i]
	        if nx >= 0 and nx < dimX and ny >= 0 and ny < dimY:
	            if maze[ny][nx] == 0:
	                ctr = 0 # of occupied neighbors must be 1
	                for j in range(4):
	                    ex = nx + dx[j]; ey = ny + dy[j]
	                    if ex >= 0 and ex < dimX and ey >= 0 and ey < dimY:
	                        if maze[ey][ex] == 1: ctr += 1
	                if ctr == 1: nlst.append(i)

	    # if 1 or more neighbors available then randomly select one and move
	    if len(nlst) > 0:
	        ir = nlst[random.randint(0, len(nlst) - 1)]
	        cx += dx[ir]; cy += dy[ir]; maze[cy][cx] = 1
	        stack.append((cx, cy, ir))
	    else: stack.pop()

	final_maze=[[0 for x in range(len(maze)+2)] for y in range(len(maze)+2)]
	final_maze=np.array(final_maze)

	maze=np.array(maze)	

	final_maze[1:final_maze.shape[0]-1,1:final_maze.shape[1]-1]= maze[0:maze.shape[0],0:maze.shape[1]]

	# Create empty corners so that the robots can start in corners

	final_maze[1][1] = 1
	final_maze[1][dimX] = 1
	final_maze[dimY][1] = 1
	final_maze[dimY][dimX] = 1

	if dimX>=15:
		# Make certain random positions empty so as to make connections between two hallways as in actual building
		openRandomPassage(final_maze, 1, dimX/2, 1, dimY/2)
		openRandomPassage(final_maze, dimX/2, dimX, 1, dimY/2)
		openRandomPassage(final_maze, 1, dimX/2, dimY/2, dimY)
		openRandomPassage(final_maze, dimX/2, dimX, dimY/2, dimY)
		openRandomPassage(final_maze, dimX/4, 3*dimX/4, dimY/4, 3*dimY/4)

	for i in range (len(final_maze)):
		for j in range(len(final_maze)):
			if final_maze[i, j]==0:
				final_maze[i, j]=1
			else:
				final_maze[i, j]=0
	
	# paint the maze
	for ky in range(imgy):
	    for kx in range(imgx):
	        pixels[kx, ky] = color[final_maze[final_maze.shape[1]*ky/imgy, final_maze.shape[0]*kx/imgx]]
	image.save("Original Maze.png", "PNG")
	
	return final_maze.tolist()