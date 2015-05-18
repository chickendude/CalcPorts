import pygame
import time
import random

# constants
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_DOWN = pygame.K_DOWN
K_UP = pygame.K_UP
K_ESCAPE = pygame.K_ESCAPE
# create some colors
black = (0,0,0)
white = (255,255,255)
#red = (255,0,0)
# object data
tile_size = 16
spike_speed = 7
width = 12
height = 8
display_w = tile_size*width
display_h = tile_size*height

# set up pygame
pygame.init()
# create our surface
gameDisplay = pygame.display.set_mode((display_w,display_h))
# set title
pygame.display.set_caption('Block Dude')
clock = pygame.time.Clock()

# load sprites
blockdude = [False]
blockdude.append(pygame.image.load('blockdudeR.bmp').convert())
blockdude.append(pygame.image.load('blockdudeL.bmp').convert())
block = pygame.image.load('block.bmp').convert()
block2 = pygame.image.load('block2.bmp').convert()
door = pygame.image.load('door.bmp').convert()

WALKABLE = (' ','D')

def blitSprite(sprite,x,y):
	gameDisplay.blit(sprite,(x,y))

def text_objects(text,font):
	''' 
	takes a string and a pygame font object
	creates and returns a text object
	'''
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf',15)
	lines = text.split('\n')
	row = 0
	for line in lines:
		TextSurf, TextRect = text_objects(line,largeText)
		TextRect.center = ((display_w/2),(display_h/2+row))
		gameDisplay.blit(TextSurf, TextRect)
		row += 75
	pygame.display.update()

class Player:
	def __init__(self,x=0,y=0):
		self.x = x
		self.y = y
		self.block = False
		self.direction = -1		# -1 = left, 1 = right
	def draw(self,level):
		x = (self.x-level.map_x)*16
		y = (self.y-level.map_y)*16
		blitSprite(blockdude[self.direction],x,y)
		if self.block:
			blitSprite(block2,x,y-16)

class Level:
	def __init__(self,level=0):
		self.level = level

	def loadLevel(self,level):
		self.level = level
		self.tilemap = []
		with open('levels.bd') as mapfile:
			maps = mapfile.read()
			levels = maps.split('#')
		defines,tilemap = levels[level].split('\n',1)
		self.map_x,self.map_y,self.map_w,self.map_h,player_x,player_y = map(int,defines.split(','))
		tilemap = tilemap.split('\n')
		for y in range(0,self.map_h):
			self.tilemap.append([])
			for x in range(0,self.map_w):
				self.tilemap[y].append(tilemap[y][x])
		return (player_x,player_y)
	
	def drawMap(self):
		map_top = self.map_y
		map_bottom = map_top+height
		if map_bottom > self.map_h:
			map_bottom = self.map_h
		sprite_y = 0
		for y in range(map_top,map_bottom):
			sprite_x = 0
			for x in range(self.map_x,self.map_x+width):
				sprite = False
				if self.tilemap[y][x] == 'B':
					sprite = block
				if self.tilemap[y][x] == 'O':
					sprite = block2
				if self.tilemap[y][x] == 'D':
					sprite = door
				if sprite:
					blitSprite(sprite,sprite_x,sprite_y)
				sprite_x += tile_size
			sprite_y += tile_size

def main():
	level = Level()
	player = Player()
	player.x,player.y = level.loadLevel(0) # loadLevel returns player's starting x/y
	score = 0
	gameExit = False
	
	while not gameExit:
		move_x = False
		move_y = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == K_LEFT:
					player.direction = -1
					if level.tilemap[player.y][player.x-1] in WALKABLE:
						if not player.block or level.tilemap[player.y-1][player.x+player.direction] in WALKABLE:
							move_x = True
				if event.key == K_RIGHT:
					player.direction = 1
					if level.tilemap[player.y][player.x+1] in WALKABLE:
						if not player.block or level.tilemap[player.y-1][player.x+player.direction] in WALKABLE:
							move_x = True
				if event.key == K_UP:
					if level.tilemap[player.y][player.x+player.direction] not in WALKABLE:
						if level.tilemap[player.y-1][player.x+player.direction] in WALKABLE and level.tilemap[player.y-1][player.x] in WALKABLE:
							# make sure the area above player and block is clear
							if not player.block or level.tilemap[player.y-2][player.x] in WALKABLE and level.tilemap[player.y-2][player.x+player.direction] in WALKABLE:
								move_x = True
								move_y = True
				if event.key == K_DOWN:
					if player.block:
						# if player is holding a block, find next empty space next to player
						if level.tilemap[player.y-1][player.x+player.direction] == ' ':
							y = player.y-1
							x = player.x+player.direction
							while level.tilemap[y+1][x] == ' ':
								y += 1
							level.tilemap[y][x] = 'O'
							player.block = False
					elif level.tilemap[player.y][player.x+player.direction] == 'O' and level.tilemap[player.y-1][player.x] in WALKABLE and level.tilemap[player.y-1][player.x+player.direction] in WALKABLE:
						# if player isn't holding a block, pick the block up
						level.tilemap[player.y][player.x+player.direction] = ' '
						player.block = True
			if move_x:
				player.x += player.direction
				if player.direction == -1:
					if player.x-level.map_x <= width/2 and level.map_x > 0:
						level.map_x -= 1
				else:
					if player.x-level.map_x >= width/2 and level.map_x < level.map_w - width:
						level.map_x += 1
			if move_y:
				player.y -= 1
				if player.y-level.map_y < height/2 and level.map_y > 0:
					level.map_y -= 1

		# check if block dude is in the air
		while level.tilemap[player.y+1][player.x] in WALKABLE:
			player.y += 1
			if player.y-level.map_y > height/2 and level.map_y < level.map_h - height:
				level.map_y += 1

		# check if we've reached the door
		while level.tilemap[player.y][player.x] == 'D':
			player.x,player.y = level.loadLevel(level.level+1)

		keys = pygame.key.get_pressed()
		if keys[K_ESCAPE]:
			gameExit = True

		# erase screen
		gameDisplay.fill(white)

		# update screen
		player.draw(level)
		level.drawMap()
		pygame.display.update()

		clock.tick(60)
	pygame.quit()

main()
