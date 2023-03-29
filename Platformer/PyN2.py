import pygame
from pygame.locals import *
import numpy
import ladder
import sys


WIDTH = 1000
HEIGHT = 1000
BACKGROUND = (0, 0, 0)




class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("p1_jump.png")

        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1, 12)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 1
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, boxes):
        hsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_UP] and onground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up
            self.jump_animation()
            self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(hsp, self.vsp, boxes)

    def move(self, x, y, boxes):
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide


class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)

class RedObject(Sprite):
    def __init__(self, startx, starty):
        super().__init__("RedObject.png", startx, starty)

class Deathbox(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Deathbox.png", startx, starty)

    def update(self, boxes):
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0 or self.x >= resolution[0]:
            self.dx *= -1
        if self.y <= 0 or self.y >= resolution[1]:
            self.dy *= -1


class Ladder(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Ladder.png", startx, starty)
        image = pygame.Surface((60, 300))
        image.fill(pygame.Color('blue'))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(950, 880)

    boxes = pygame.sprite.Group()
    for bx in range(35, 450, 70):
        boxes.add(Box(bx, 450))

    for bx in range(35, 1100, 70):
        boxes.add(Box(bx, -35))

    for bx in range(35, 400, 70):
        boxes.add(Box(bx, 800))

    for bx in range(35, 1100, 70):
        boxes.add(Box(bx, 1035))

    for bx in range(35, 1100, 70):
        boxes.add(Box(bx, 965))

    for bx in range(35, 1100, 70):
        boxes.add(Box(1035, bx))

    for bx in range(35, 1100, 70):
        boxes.add(Box(-35, bx))

    for bx in range(-15, 1100, 70):
        boxes.add(Box(bx, 105))

    boxes.add(Box(965, 175)) # \
    boxes.add(Box(965, 245)) #  Лестница
    boxes.add(Box(965, 315)) # /
    boxes.add(Box(965, 385)) #/
    boxes.add(Box(965, 650)) #\
    boxes.add(Box(895, 650)) # \
    boxes.add(Box(825, 650)) #  \
    boxes.add(Box(755, 650)) #   Правая нижняя платформа
    boxes.add(Box(685, 650)) #  /
    boxes.add(Box(615, 650)) #/
    boxes.add(Box(895, 385)) #\
    boxes.add(Box(825, 385)) # Правая верхняя платформа
    boxes.add(Box(755, 385)) #/
    boxes.add(Deathbox(760, 500))
    boxes.add(RedObject(500, 900))





    while True:
        pygame.event.pump()
        player.update(boxes)

        # Draw loop
        screen.fill(BACKGROUND)

        if Player.rect.colliderect(RedObject.rect):
            print('collision!')
        player.draw(screen)
        boxes.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()


if __name__ == "__main__":
    main()