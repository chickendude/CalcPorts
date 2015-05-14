import pygame
import time
import random

# constants
display_w = 800
display_h = 600
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_DOWN = pygame.K_DOWN
K_UP = pygame.K_UP
K_ESCAPE = pygame.K_ESCAPE
# create some colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
# object data
tile_size = 16
spike_speed = 7

# set up pygame
pygame.init()
# create our surface
gameDisplay = pygame.display.set_mode((display_w,display_h))
# set title
pygame.display.set_caption('Avalanche')
clock = pygame.time.Clock()

# load sprites
sprite = pygame.image.load('man.bmp')
spike_sprite = []
spike_sprite.append(pygame.image.load('spike1.bmp'))
spike_sprite.append(pygame.image.load('spike2.bmp'))
spike_sprite.append(pygame.image.load('spike3.bmp'))

spikes = []

def blitSprite(sprite,x,y):
	# this is for transparency
	surface = pygame.Surface((16,16), depth=24)
	surface.set_alpha(255)
	surface.set_colorkey(red)
	surface.blit(sprite,(0,0))
	gameDisplay.blit(surface,(x,y))

def text_objects(text,font):
	''' 
	takes a string and a pygame font object
	creates and returns a text object
	'''
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf',75)
	lines = text.split('\n')
	row = 0
	for line in lines:
		TextSurf, TextRect = text_objects(line,largeText)
		TextRect.center = ((display_w/2),(display_h/2+row))
		gameDisplay.blit(TextSurf, TextRect)
		row += 75
	pygame.display.update()

def drawSpikes(spike_array):
	for spike in spike_array:
		x = spike[0]
		y = spike[1]
		frame = spike[2]
		timer = spike[3]
		if frame >= 0:
			blitSprite(spike_sprite[frame],x,y)

def main():
	score = 0
	gameExit = False

	player_x = (display_w//2)
	player_y = (display_h-tile_size)

	# build spike array
	for i in range(display_w//16):
		x = i*16
		y = 0
		frame = -1
		timer = random.randint(10,300)
		spikes.append([x,y,frame,timer])

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			player_x -= 4
		if keys[K_RIGHT]:
			player_x += 4
		if keys[K_UP]:
			player_y -= 4
		if keys[K_DOWN]:
			player_y += 4
		if keys[K_ESCAPE]:
			gameExit = True

		# update object
		for i in range(len(spikes)):
			x = spikes[i][0]
			y = spikes[i][1]
			frame = spikes[i][2]
			timer = spikes[i][3]
			if frame < 2:
				timer -= 1
				if timer <= 0:
					timer = random.randint(10,100)
					frame += 1
			elif frame == 2:
				y += spike_speed
			if y > display_h:
				y = 0
				frame = -1
				timer = random.randint(10,332)
			spikes[i][0] = x
			spikes[i][1] = y
			spikes[i][2] = frame
			spikes[i][3] = timer
			
		# update player
		if player_x > display_w-tile_size:
			message_display("don't run away!")
			time.sleep(1)
			player_x = display_w-tile_size
		if player_x < 0:
			message_display("don't run away!")
			time.sleep(1)
			player_x = 0

		if player_y > display_h-tile_size:
			player_y = display_h-tile_size
		if player_y < 0:
			player_y = 0

		gameDisplay.fill(white)
		blitSprite(sprite,player_x,player_y)
		drawSpikes(spikes)

		pygame.display.update()

		# check collision
		for spike in spikes:
			obj_x = spike[0]
			obj_y = spike[1]
			if (obj_x < player_x+tile_size and obj_x >= player_x) or (obj_x+tile_size > player_x and obj_x < player_x):
				if (obj_y < player_y+tile_size and obj_y >= player_y) or (obj_y+tile_size > player_y and obj_y < player_y):
					message_display("you loze!\nscore: "+str(score))
					time.sleep(1)
					gameExit = True
		score += 10
		clock.tick(60)
	pygame.quit()

main()
