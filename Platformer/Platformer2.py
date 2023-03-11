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


def main():
	pygame.init()  # Инициация PyGame, обязательная строчка
	screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
	pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
	bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
	# будем использовать как фон
	bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

	while 1:  # Основной цикл программы
		for e in pygame.event.get():  # Обрабатываем события
			if e.type == QUIT:
				raise SystemExit("QUIT")
		screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
		pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
	main()

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