import cfg, os, pygame, sys
from pygame.locals import *

class GameStart(object):
	def __init__(self, SCR_WIDTH, SCR_HEIGHT):
		self.options = ['START', 'HIGH SCORES', 'QUIT']
		self.up, self.down, self.enter, self.start, self.quit = False, False, False, False, False
		resource_path = cfg.resource_path
		self.titleFont = pygame.font.Font(os.path.join(resource_path, 'joystix monospace.ttf'), 42)
		self.optionFont = pygame.font.Font(os.path.join(resource_path, 'joystix monospace.ttf'), 24)
		self.selected = 0

		
	def check_events(self, kevents):
		for event in kevents:
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					self.enter = True
				elif event.key == K_ESCAPE:
					self.quit = True
				elif event.key == K_UP:
					self.up = True
				elif event.key == K_DOWN:
					self.down = True
			if event.type == KEYUP:
				if event.key == K_RETURN:
					self.enter = False
				elif event.key == K_ESCAPE:
					self.quit = False
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
				return 1	# Return gameplay scene code
			elif self.selected == 1:
				return 3 	# Return highscore scene code	
			elif self.selected == 2:
				return 4 	# Return game end code
		return 0	# Return current scene code

	def render(self, background):
		titleText = self.titleFont.render('SPACE SHOOTER V3', True, (255,255,255))
		titleRect = titleText.get_rect()
		titleRect.centerx = background.get_rect().centerx
		background.blit(titleText, titleRect)
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