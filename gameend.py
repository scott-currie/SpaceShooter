import cfg
import os
import pygame
from pygame.locals import *


class GameEnd(object):
	def __init__(self, SCR_WIDTH, SCR_HEIGHT):
		self.up, self.down, self.enter = False, False, False
		self.options = ['Play Again', 'Return to Main Menu', 'Quit']
		resource_path = cfg.resource_path
		self.titleFont = pygame.font.Font(os.path.join(resource_path, 'joystix monospace.ttf'), 42)
		self.optionFont = pygame.font.Font(os.path.join(resource_path, 'joystix monospace.ttf'), 24)
		self.selected = 0
		self.score = cfg.playerScore

	def check_events(self, kevents):
		for event in kevents:
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					self.enter = True
				elif event.key == K_UP:
					self.up = True
				elif event.key == K_DOWN:
					self.down = True
			if event.type == KEYUP:
				if event.key == K_RETURN:
					self.enter = False
				elif event.key == K_UP:
					self.up = False
				elif event.key == K_DOWN:
					self.down = False

	def update(self, kevents):
		self.check_events(kevents)
		if self.up:
			self.selected -= 1
			self.up = False
		elif self.down:
			self.selected += 1
			self.down = False
		if self.selected >= len(self.options):
			self.selected = 0
		elif self.selected < 0:
			self.selected = len(self.options) - 1
		elif self.enter:
			self.enter = False
			if self.selected == 0:
				return 1  # Return gameplay scene code
			elif self.selected == 1:
				return 0 	# Return gamestart scene code
			elif self.selected == 2:
				return 4 	# Return game quit code
		return 2  # Return current scene code

	def render(self, background):
		titleText = self.titleFont.render('Game Over', True, (255,255,255))
		titleRect = titleText.get_rect()
		titleRect.centerx = background.get_rect().centerx
		background.blit(titleText, titleRect)
		scoreText = self.titleFont.render(str(self.score), True, (255,255,255))
		scoreTextRect = scoreText.get_rect()
		scoreTextRect.top = titleRect.bottom
		scoreTextRect.centerx = background.get_rect().centerx
		background.blit(scoreText, scoreTextRect)
		for option in self.options:
			if self.options.index(option) == self.selected:
				color = (255,255,0)
			else:
				color = (255,255,255)
			optionText = self.optionFont.render(option, True, color)
			optionRect = optionText.get_rect()
			optionRect.centerx = background.get_rect().centerx
			optionRect.centery = background.get_rect().centery + (self.options.index(option) * optionRect.height)
			background.blit(optionText, optionRect)