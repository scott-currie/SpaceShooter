import cfg, sys
from imageloader import ImageLoader
import os
import pygame

class Player(pygame.sprite.Sprite):
	BULLET_SPEED = 9
	SHOT_DELAY = 10
	MAX_LIVES = 3
	SAFE_TIME = cfg.FPS * 3
	MOVE_SPEED = 10	

	def __init__(self, SCR_WIDTH=640, SCR_HEIGHT=480):
		pygame.sprite.Sprite.__init__(self)
		self.SCR_WIDTH = SCR_WIDTH
		self.SCR_HEIGHT = SCR_HEIGHT
		resource_path = cfg.resource_path
		img_ship_1 = ImageLoader.load(resource_path, 'ship.png', 2.0)
		img_ship_2 = ImageLoader.load(resource_path, 'ship2.png', 2.0)
		self.images = [img_ship_1, img_ship_2]
		self.image = self.images[0]
		self.imgShot = ImageLoader.load(resource_path, 'player_shot.png', 1.0)
		self.rect = self.image.get_rect()
		self.rect.centerx = self.SCR_WIDTH / 2
		self.rect.bottom = self.SCR_HEIGHT
		self.bullets = []
		self.shot_delay = 0
		self.score = 0
		self.lives = Player.MAX_LIVES
		self.fire_sound = pygame.mixer.Sound(os.path.join(resource_path, 'laser1.wav'))
		self.fire_sound.set_volume(.01)
		self.safe_time = Player.SAFE_TIME 	# New player starts "safe"
		self.left, self.right, self.fire, self.safe = False, False, False, False
	
	def fire_bullet(self):
		if self.shot_delay <= 0:
			self.fire_sound.play()
			bullet = pygame.Rect.copy(self.imgShot.get_rect())
			bullet.center = self.rect.centerx, self.rect.top
			self.bullets.append(bullet)
			self.shot_delay = Player.SHOT_DELAY
	
	def update_bullets(self):
		# Move bullets 
		for bullet in self.bullets:
			bullet.y -= Player.BULLET_SPEED
		# Kill dead bullets
		if bullet.bottom <= 0:
			self.bullets.remove(bullet)

	def render_bullets(self, screen):
		for bullet in self.bullets:
			screen.blit(self.imgShot, bullet)

	def update(self):
		#--- Update player ---#
		self.shot_delay -= 1
		# self.safe_time -= 1
		if self.right and self.rect.x < self.SCR_WIDTH - 1 - self.rect.width - Player.MOVE_SPEED:	
			self.rect.x += Player.MOVE_SPEED
		if self.left and self.rect.x > Player.MOVE_SPEED:	
			self.rect.x -= Player.MOVE_SPEED	
		if self.fire and self.safe_time <= 0:
			self.fire_bullet()
		# Any bullets? Update them.
		if self.bullets:
			self.update_bullets()
		# Do blink animation
		if self.safe_time > 0:
			self.image = self.get_image()
		else:
			self.image = self.images[0]

	def get_image(self):
		# Toggle ship image every 5 updates
		if self.safe_time % 5 == 0:
			return self.images[1 - self.images.index(self.image)]
		else:
			return self.image

	def render(self, screen):
		screen.blit(self.image, self.rect)



