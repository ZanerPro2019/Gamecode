import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Платформер')

player = pygame.image.load('idle.png')
bg = pygame.image.load('bg.jpg')
platform = pygame.image.load('platform.png')

x = 400
y = 400
speed = 1

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super.__init__()
		self.image = pygame.image.load('idle.png')
		self.rect = self.image.get_rect()

		self.change_x = 0
		self.change_y = 0

	def jump(self):
		self.rect.y += 10
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 10

		if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
			self.change_y = -16

	def update(self):
		self.calc_gravity()

		self.rect.x += self.change_x

		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				self.rect.left = block.rect.right

				# Передвигаемся вверх/вниз
		self.rect.y += self.change_y

		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom
			self.change_y = 0

	def calc_grav(self):
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += .95

		if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = SCREEN_HEIGHT - self.rect.height

	def jump(self):
		self.rect.y += 10
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 10

		if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
			self.change_y = -16

	def go_left(self):
		self.change_x = -9
		if (self.right):
			self.flip()
			self.right = False

	def go_right(self):
		self.change_x = 9
		if (not self.right):
			self.flip()
			self.right = True

	def stop(self):
		self.change_x = 0

	def flip(self):
		self.image = pygame.transform.flip(self.image, True, False)

class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		super().__init__()
		self.image = pygame.image.load('platform.png')

		self.rect = self.image.get_rect()


class Level(object):
	def __init__(self, player):
		self.platforms = pygame.sprite.Group()
		self.player = player

		self.background = None

	def update(self):
		self.platform_list.update()

	def draw(self, screen):
		screen.blit(bg, (0, 0))

		self.platform_list.draw(screen)


class Level_01(Level):
	def __init__(self, player):
		Level.__init__(self, player)

		level = [
			[210, 32, 500, 500],
			[210, 32, 200, 400],
			[210, 32, 600, 300],
		]

		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)

clock = pygame.time.Clock()
run = True
while(run):
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT]:
		x -= speed
	elif keys[pygame.K_RIGHT]:
		x += speed
	elif keys[pygame.K_UP]:
		y -= speed
	elif keys[pygame.K_DOWN]:
		y += speed
	win.blit(bg, (0, 0))
	win.blit(player, (x, y))
	pygame.display.update()

pygame.quit()