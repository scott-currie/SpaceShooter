import os, cfg
import pygame
from pygame.locals import *

class HighScoreReader(object):
	@staticmethod
	def get_scores():
		resource_path = cfg.resource_path
		with open(os.path.join(resource_path, 'highscores.txt'), 'r') as inFile:
			scores = inFile.read().split('\n')
			scores = [score.split(',') for score in scores]
			scores = sorted(scores, key=lambda s: s[1], reverse=True)
			return scores

class HighScore(object):
	def __init__(self, SCR_WIDTH, SCR_HEIGHT):
		self.SCR_WIDTH = SCR_WIDTH
		self.SCR_HEIGHT = SCR_HEIGHT
		self.up, self.down, self.enter = False, False, False
		self.scores = HighScoreReader.get_scores()
		resource_path = cfg.resource_path
		self.titleFont = pygame.font.Font(os.path.join(resource_path, 'joystix monospace.ttf'), 48)
		self.scoresFont = pygame.font.Font(os.path.join(resource_path, 'joystix monospace.ttf'), 24)

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
		if self.enter:
			return 0	# Return gamestart scene code
		else:
			return 3	# Return current scene code

	def render(self, background):
		centerx = background.get_rect().centerx
		title = self.titleFont.render('High Scores', True, (255,255,255))
		titleRect = title.get_rect()
		titleRect.centerx = centerx
		background.blit(title, titleRect)
		for score in self.scores:
			scoreName = self.scoresFont.render(score[0], True, (255,255,255))
			scoreScore = self.scoresFont.render(score[1], True, (255,255,255))			
			rowPos = titleRect.bottom + self.scores.index(score) * scoreName.get_rect().height			
			scoreNameRect = scoreName.get_rect()
			scoreNameRect.top = rowPos
			scoreNameRect.width = 100
			scoreScoreRect = scoreScore.get_rect()
			scoreScoreRect.top = rowPos
			scoreScoreRect.left = scoreNameRect.right 
			background.blit(scoreName, scoreNameRect)
			background.blit(scoreScore, scoreScoreRect)
		footer = self.scoresFont.render('Press ENTER to return.', True, (255,255,255))
		footerRect = footer.get_rect()
		footerRect.bottom = background.get_rect().height
		footerRect.centerx = centerx
		background.blit(footer, footerRect)




