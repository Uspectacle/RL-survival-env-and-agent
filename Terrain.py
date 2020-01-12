import numpy as np
import matplotlib as plt
from graphics import *
import random
import math

class World :
	def __init__(self, size):
		self.SIZE_OBS = 1
		self.number_of_different_blocks = 3
		self.SIZE = size
		self.num_actions = 4
		self.grid = [[0 for i in range(self.SIZE)] for j in range(self.SIZE)]
		self.tmpBlock = 0
		self.done = False

class Tree :
	def __init__(self):
		self.age = 0

class Ground :
	def __init__(self):
		self.age = 0
class Hole :
	def __init__(self):
		self.age = 0

class Player : 
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.age = 0
		self.reward = 0

def InitWorld(world):
	#Ground everywhere
	for i in range(world.SIZE):
		for j in range(world.SIZE):
			world.grid[i][j] = Ground()
	#Some trees
	for i in range(world.SIZE):
		for j in range(world.SIZE):
			if(random.randint(0, 200) > 199):
				world.grid[i][j] = Tree()
	#Forests
	for i in range(1, world.SIZE-1):
		for j in range(1, world.SIZE-1):
			if(HasTreeNeighbours(world.grid, i, j)):
				if(random.randint(0, 10) > 3):
					world.grid[i][j] = Tree()
	#Holes
	for i in range(1, world.SIZE-1):
		for j in range(1, world.SIZE-1):
			if(random.randint(0, 100) > 90):
				world.grid[i][j] = Hole()
	#Player in the middle (if there isn't a hole)
	x = math.floor(world.SIZE/2)
	y = math.floor(world.SIZE/2)
	while type(world.grid[x][y]) is Hole : 
		x+=1
	player = Player(x, y)
	#before replacing a block by the player, remember what was the block in tmpBlock
	world.tmpBlock = world.grid[x][y]
	world.grid[x][y] = player
	#print("Initial position of player : ", player.x, player.y, "\n")
	return player

def HasTreeNeighbours(grid, posX, posY):
	if(type(grid[posX-1][posY]) is Tree or
		type(grid[posX][posY-1]) is Tree or
		type(grid[posX+1][posY]) is Tree or
		type(grid[posX][posY+1]) is Tree):
		return True
	else: 
		return False

def ColorTheRect(bloc, rect):
	if(type(bloc) is Tree):
		rect.setFill(color_rgb(50,205,50))
	if(type(bloc) is Ground):
		rect.setFill(color_rgb(139,69,19))
	if(type(bloc) is Hole):
		rect.setFill(color_rgb(0,0,0))
	if(type(bloc) is Player):
		rect.setFill(color_rgb(230,10,10))

def Display_World(world, win, obs, init):
	RECT_SIZE = 8
	
	if init :
		win = GraphWin("Environment", 800, 800)
		win.setBackground(color_rgb(0,0,0))

	for i in range(len(world.grid)):
		for j in range(len(world.grid[i])):
			rect = Rectangle(Point(RECT_SIZE*i, RECT_SIZE*j), 
				Point(RECT_SIZE*i + RECT_SIZE, RECT_SIZE*j + RECT_SIZE))
			ColorTheRect(world.grid[i][j], rect)
			rect.draw(win)

	#print('len obs : ', len(obs)**2)
	for i in range(world.SIZE_OBS + 2):
		for j in range(world.SIZE_OBS + 2):
			rect = Rectangle(Point(RECT_SIZE*i + 300, RECT_SIZE*j + 300), 
				Point(RECT_SIZE*i + RECT_SIZE + 300, RECT_SIZE*j + RECT_SIZE + 300))
			ColorTheRect(obs[i][j], rect)
			rect.draw(win)
			#print('obs number ', k, ' is ', type(obs[k]))
	#win.getMouse()
	time.sleep(5)
	#win.close()
	return win

def Update_Env(world, player, action):
	#right
	if action == 1 and player.x + 1 < len(world.grid):
		#print('right')
		#Replace the player's former block
		world.grid[player.x][player.y] = world.tmpBlock
		#UpdatePos
		player.x += 1
		#Save block under player
		world.tmpBlock = world.grid[player.x][player.y]
		#Place player
		world.grid[player.x][player.y] = player
	#Left
	elif action == 2 and player.x - 1 > 0:
		#print('left')
		world.grid[player.x][player.y] = world.tmpBlock
		player.x -= 1
		world.tmpBlock = world.grid[player.x][player.y]
		world.grid[player.x][player.y] = player
	#Up
	elif action == 3 and player.y + 1 > 0:
		#print('up')
		world.grid[player.x][player.y] = world.tmpBlock
		player.y -= 1
		world.tmpBlock = world.grid[player.x][player.y]
		world.grid[player.x][player.y] = player
	#Down
	elif action == 0 :
		#print('down')
		if player.y + 1 < len(world.grid):
			world.grid[player.x][player.y] = world.tmpBlock
			player.y += 1
			world.tmpBlock = world.grid[player.x][player.y]
			world.grid[player.x][player.y] = player

def Action_On_Env(world, player, action):
	#UpdateWorld
	Update_Env(world, player, action)

	#GiveReward end the game if needed
	if type(world.tmpBlock) is Hole:
		#print('AAAAH !! A hole !!')
		player.reward -= 300
		world.done = True
	else:
		player.reward += 1
	return Give_Obs(world, player), player.reward

def Give_Obs(world, player):
	obs = [[0 for x in range(world.SIZE_OBS*2 + 1)] for y in range(world.SIZE_OBS*2 + 1)] 
	
	for i in range(world.SIZE_OBS*2 + 1):
		for j in range(world.SIZE_OBS + 2):
			if player.x + i - 1 < world.SIZE and player.y + j - 1 < world.SIZE and player.x + i - 1 > 0 and player.y + j - 1 > 0 :
				if i == 1 and j == 1 :
					obs[i][j] = world.tmpBlock
				else :
					obs[i][j] = world.grid[player.x + i - 1][player.y + j - 1]
			else :
				hole = Hole()
				obs[i][j] = hole
	return obs
		
def StartEnv(SIZE):
	world = World(SIZE)
	player = InitWorld(world)
	obs = Give_Obs(world, player)
	return world, player, obs