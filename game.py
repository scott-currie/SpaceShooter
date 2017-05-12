import cfg
from gamestart import GameStart
from gameend import GameEnd
from gameplay import GamePlay
from highscore import HighScore
import os, pygame, random, sys
from pygame.locals import *

#--- Game constants
SCR_WIDTH, SCR_HEIGHT = 800, 600
FPS = 30

# #--- pygame setup ---#
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
background.convert()

scene = GameStart(SCR_WIDTH, SCR_HEIGHT)
playerScore = 0

#--- Game loop ---#
fps_clock = pygame.time.Clock()

run = True
while run:
	# Get events
	keys = []
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		# Collect key events to pass to scene updates
		if e.type == KEYDOWN or e.type == KEYUP:
			keys.append(e)
	# Update scene
	sceneIndex = scene.update(keys)
	if sceneIndex == 0:
		if type(scene) is not GameStart:
			scene = GameStart(SCR_WIDTH, SCR_HEIGHT)
	elif sceneIndex == 1:
		if type(scene) is not GamePlay:
			scene = GamePlay(SCR_WIDTH, SCR_HEIGHT)
	elif sceneIndex == 2:
		if type(scene) is not GameEnd:
			scene = GameEnd(SCR_WIDTH, SCR_HEIGHT) 
	elif sceneIndex == 3:
		if type(scene) is not HighScore:
			scene = HighScore(SCR_WIDTH, SCR_HEIGHT)
	elif sceneIndex == 4:
		run = False

	# Render scene
	background.fill((0, 0, 0))
	scene.render(background)

	screen.blit(background, (0, 0))
	pygame.display.flip()
	fps_clock.tick(FPS)
pygame.quit()
sys.exit()
