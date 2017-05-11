from imageloader import ImageLoader
import os, sys, cfg
import pygame
import random

class Enemy(pygame.sprite.Sprite):
	MIN_MOVE_SPEED = 3
	MAX_MOVE_SPEED = 6
	ANIMATION_DURATION = 30	
	bullets = []
	BULLET_SPEED = 6
	ATK_FREQ = .99
	ATK_DELAY = 25	
	VERT_MOVE = 80
	V_MOVE_SPEED = 4
	# Percentage of screen height enemies can occupy
	LOWER_SPAWN_BOUNDARY = .66

	def __init__(self, SCR_WIDTH, SCR_HEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.SCR_WIDTH = SCR_WIDTH
		self.SCR_HEIGHT = SCR_HEIGHT
		resource_path = cfg.resource_path
		image_1 = ImageLoader.load(resource_path, 'alien.png', 1.7)
		image_2 = ImageLoader.load(resource_path, 'alien2.png', 1.7)
		self.images = [image_1, image_2]
		if random.random() > .5:
			self.image = self.images[0]
		else:
			self.image = self.images[1]
		self.imgShot = ImageLoader.load(resource_path, 'enemy_shot.png', 1.0)
		self.rect = self.images[0].get_rect()
		self.init_start_state()
		self.shot_delay = 0
		self.animation_timer = self.ANIMATION_DURATION
		self.snd_fire = pygame.mixer.Sound(os.path.join(resource_path, 'alien_fire.wav'))
		self.snd_fire.set_volume(.01)
		self.fire_delay = 0
		self.rising = True
	  
	def init_start_state(self):
		''' Set horizontal speed and direction'''
		self.hMoveSpeed = random.randint(Enemy.MIN_MOVE_SPEED, Enemy.MAX_MOVE_SPEED + 1)
		if random.random() > .5:
			self.rect.x = self.SCR_WIDTH
			self.hMoveSpeed = -self.hMoveSpeed
		else:
			self.rect.right = 0	
		''' Are we rising or falling on start? '''
		if random.random() > .5:
			self.rising = False
		''' Get a starting y position within the allowable range'''
		self.rect.y = random.randint(Enemy.VERT_MOVE, Enemy.LOWER_SPAWN_BOUNDARY * self.SCR_HEIGHT - Enemy.VERT_MOVE)
		self.vRange = self.rect.y + Enemy.VERT_MOVE, self.rect.y - Enemy.VERT_MOVE		
		randYShift = random.randint(0,Enemy.VERT_MOVE)
		if random.random() > .5:
			randYShift = -randYShift
		self.rect.y += randYShift
		self.vMoveSpeed = Enemy.V_MOVE_SPEED	

	def fire_bullet(self):
		# Play pew sound
		self.snd_fire.play()
		''' Bullet is a Rect copied from shot image, centered on center bottom 
		of enemy Rect'''
		bullet = pygame.Rect.copy(self.imgShot.get_rect())
		bullet.center = self.rect.centerx, self.rect.bottom
		Enemy.bullets.append(bullet)
		self.fire_delay = Enemy.ATK_DELAY

	def update_bullets(self):
		for bullet in Enemy.bullets:
			bullet.y += Enemy.BULLET_SPEED
		if bullet.y > self.SCR_HEIGHT:
			Enemy.bullets.remove(bullet)

	def render(self, screen):
		screen.blit(self.image, (self.rect.x, self.rect.y))

	def update(self, player):
		self.fire_delay -= 1
		""" Choose current image """
		# Decrement animation timer
		self.animation_timer -= 1
		# Toggle image if animation_timer less than 0
		if self.animation_timer <= 0:
			# Reset animation timer
			self.animation_timer = Enemy.ANIMATION_DURATION
			# Toggle ship image. 1 - item index toggles 0 <-> 1 for 2 item list
			self.image = self.images[ 1 - self.images.index(self.image)]
		
		""" Do horizontal movement """
		self.rect.x += self.hMoveSpeed		
		if self.rect.x > self.SCR_WIDTH:
			self.rect.x = 0
		elif self.rect.right < 0:
			self.rect.left = self.SCR_WIDTH
		
		""" Do vertical movement """
		if self.rising:
			if self.rect.top >= self.vRange[1]:
				self.rect.y -= self.vMoveSpeed 
			else:
				self.rising = False
		else:
			if self.rect.bottom < self.vRange[0]:
				self.rect.y += self.vMoveSpeed
			else:
				self.rising = True

		""" Do shooting """
		if player.safe_time <= 0 and self.fire_delay <= 0:
		#Can fire bullet
			if random.random() > Enemy.ATK_FREQ:
				self.fire_bullet()
			#This bit ensures that enemy always fires (if shot is ready) when its centerx is between player's left and right
			elif self.rect.centerx > player.rect.left and self.rect.centerx < player.rect.right:
				self.fire_bullet()

	def render_bullets(self, screen):
		for bullet in Enemy.bullets:
			screen.blit(self.imgShot, bullet)
