import cfg
from enemy import Enemy
from imageloader import ImageLoader
import os
from player import Player
import pygame
from pygame.locals import *
import random
import sys

class GamePlay(object):
	#--- pygame setup ---#
	pygame.init()
	pygame.mixer.pre_init(44100, -16, 1, 512)
	pygame.mixer.set_num_channels(24)

	def __init__(self, SCR_WIDTH, SCR_HEIGHT):
		self.SCR_SIZE = SCR_WIDTH, SCR_HEIGHT
		self.NUM_ENEMIES = 6
		self.EFFECT_DURATION = 10
		self.NUM_STARS = 30
		self.SAFE_TIME = 90
		self.player = Player(SCR_WIDTH, SCR_HEIGHT)
		self.enemies = []
		for e in range(self.NUM_ENEMIES):
			self.enemies.append(Enemy(self.SCR_SIZE[0], self.SCR_SIZE[1]))		
		self.resource_path = cfg.resource_path
		self.effect_images = self.load_images()
		self.sounds = self.load_sounds()
		self.hud_font = pygame.font.Font(os.path.join(self.resource_path, 'joystix monospace.ttf'), 24)
		self.msg_font = pygame.font.Font(os.path.join(self.resource_path, 'joystix monospace.ttf'), 42)
		self.img_shipIcon = ImageLoader.load(self.resource_path, 'ship.png', 1.2)
		self.effects = []
		self.enemy_level_step = 20
		self.paused = False

	def load_images(self):
		img_boom_1 = ImageLoader.load(self.resource_path, 'boom.png', 2.0)
		img_boom_2 = ImageLoader.load(self.resource_path, 'boom2.png', 2.0)
		img_boom_3 = ImageLoader.load(self.resource_path, 'boom3.png', 2.0)
		return [img_boom_1, img_boom_2, img_boom_3]

	def load_sounds(self):
		snd_boom = pygame.mixer.Sound(os.path.join(self.resource_path,
													'boom.wav'))
		snd_ready = pygame.mixer.Sound(os.path.join(self.resource_path,
													'sirens.wav'))
		snd_boom.set_volume(.1)
		snd_alien_boom = pygame.mixer.Sound(os.path.join(self.resource_path,
														'alien_boom.wav'))
		snd_alien_boom.set_volume(.01)
		return {'ready': snd_ready, 'boom': snd_boom, 
				'alien_boom': snd_alien_boom}

	def check_events(self, kevents):
		for event in kevents:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					self.player.left = True
					self.player.right = False
				elif event.key == K_RIGHT:
					self.player.right = True
					self.player.left = False
				if event.key == K_SPACE:
					self.player.fire = True
				if event.key == K_p:
					self.paused = not self.paused
			if event.type == KEYUP:
				if event.key == K_RIGHT:
					self.player.right = False
				if event.key == K_LEFT:
					self.player.left = False
				if event.key == K_SPACE:
					self.player.fire = False

	def update(self, kevents):
		# Check key events for state changes
		self.check_events(kevents)
		self.player.safe_time -= 1
		if not self.paused:
			if self.player.lives > 0:
				# cfg.playerScore = self.player.score
				self.player.update()

				#--- Update game state ---#
				if self.player.score > 0:
					if self.player.score % self.enemy_level_step == 0:
						Enemy.ATK_FREQ -= .01
						self.enemy_level_step += self.enemy_level_step

				#--- Update enemies ---#
				#-- Replace dead enemies
				if len(self.enemies) < self.NUM_ENEMIES + int(self.player.score / 50):
					self.enemies.append(Enemy(self.SCR_SIZE[0], self.SCR_SIZE[1]))
				#-- Process enemy behavior rules
				for enemy in self.enemies:
					enemy.update(self.player)
				#-- Update enemy bullets, if any
				if len(Enemy.bullets) > 0:
					enemy.update_bullets()		

				#--- Update effects --#
				if len(self.effects) > 0:
					for effect in self.effects:
						if effect[2] <= 0:
							self.effects.remove(effect)
						else:
							effect[2] -= 1

				#--- Check collisions ---#
				#Check state of each self.player bullet
				deadBullets = []
				enemyRects = []
				for enemy in self.enemies:
					enemyRects.append(enemy.rect)
				deadEnemies = []
				for bullet in self.player.bullets:
					if bullet not in deadBullets:
						hitEnemy = bullet.collidelist(enemyRects)
						if hitEnemy >= 0:
							self.sounds['alien_boom'].play()								
							enemy = self.enemies[hitEnemy]
							if enemy not in deadEnemies:
								self.effects.append([enemy.rect.x, enemy.rect.y, self.EFFECT_DURATION])
								# Add collided enemy to deadEnemies to be removed later
								deadEnemies.append(enemy)
								#If bullet kills enemy, add to deadBullets for removal after all bullets checked
								deadBullets.append(bullet)
								#increment player score by 1
								self.player.score += 1
					
				#If any bullets marked for deletion due to collision
				if deadBullets:
					#Generate new bullets list of bullet from bullets not in deadBullets
					self.player.bullets = [bullet for bullet in self.player.bullets if bullet not in deadBullets]

				# If any enemies killed and marked for deletion
				if deadEnemies:
					self.enemies = [enemy for enemy in self.enemies if enemy not in deadEnemies]

				# Check state of all enemy bullets	
				deadBullets = []
				for bullet in Enemy.bullets:
					if self.player.rect.colliderect(bullet):
						self.sounds['boom'].play()
						self.effects.append([self.player.rect.x, self.player.rect.y, self.EFFECT_DURATION])
						self.player.lives -= 1
						deadBullets.append(bullet)
						self.player.safe_time = self.SAFE_TIME 
						Enemy.bullets = []
						self.player.bullets = []

				# Flush dead enemy bullets
				if deadBullets:
					Enemy.bullets = [bullet for bullet in Enemy.bullets if bullet not in deadBullets]
		else:
			pass
			""" Do special paused state stuff here """
		
		""" Decide how to end update """
		if self.player.lives > 0:
			# Lives left means keep playing
			return 1
		else:
			if self.player.safe_time > 0:
				# No lives left, but still in safe time, continue scene
				return 1
			else:
				# No lives left, no safe time, send gameend scene signal
				cfg.playerScore = self.player.score
				return 2

	def render(self, background):
		# Draw player
		self.player.render(background)
		# Draw all player bullets
		self.player.render_bullets(background)
		
		#Blit effects if any
		if len(self.effects) > 0:
			for effect in self.effects:
				if effect[2] > self.EFFECT_DURATION / 3:
					imgIndex = 0
				elif effect[2] > self.EFFECT_DURATION / 2:
					imgIndex = 1
				else:
					imgIndex = 2		
				background.blit(self.effect_images[imgIndex], (effect[0], effect[1]))
		# Render each enemy in list
		for enemy in self.enemies:
			enemy.render(background)		
		# Draw all enemy bullets collectively
		enemy.render_bullets(background)
		
		""" Set and display status message if needed """
		msg_txt = ''
		# Display paused message if in paused state
		if self.paused:
			msg_txt = 'PAUSED'
		# Message displays while player is "safe"
		elif self.player.safe_time > 0:
			if self.player.lives > 0:
				msg_txt = 'GET READY!'
			else:
				msg_txt = 'GAME OVER'
		if msg_txt:
			message = self.msg_font.render(msg_txt, 2, (255,255,255))		
			msg_pos = message.get_rect()
			msg_pos.center = background.get_rect().centerx, background.get_rect().centery
			background.blit(message, msg_pos)		

		""" Draw stats """
		# Draw player score
		player_score = self.hud_font.render(str(self.player.score), 2, (255,255,255))
		background.blit(player_score, (self.SCR_SIZE[0] / 2, 0))		
		# Draw icons for ships remaining
		for l in range(self.player.lives - 1):
			background.blit(self.img_shipIcon, (l * self.img_shipIcon.get_rect().width, 0))
		