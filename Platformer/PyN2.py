import pygame
from pygame.locals import *
import pygame as pg
import numpy
import sys
import pygame_menu
import random
kill = 0
pygame.init()


WIDTH = 1000
HEIGHT = 1000
BACKGROUND = (0, 0, 0)
bg = pygame.image.load("background.jpg")
win = pygame.display.set_mode((WIDTH, HEIGHT))




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
        ground = self.check_collision(0, 1, boxes)
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

        if key[pygame.K_UP] and ground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        # gravity
        if self.vsp < 10 and not ground:  # 9.8 rounded up
            self.jump_animation()
            self.vsp += self.gravity

        if ground and self.vsp > 0:
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
    def __init__(self, startx, starty, group='cub', action=False):
        super().__init__("boxAlt.png", startx, starty)

    def get_group(self):
        return self.group

class Teleport(Sprite):
    def __init__(self, startx, starty):
        super().__init__("RedObject.png", startx, starty)

class UsefulTeleport(Sprite):
    def __init__(self, startx, starty):
        super().__init__("green.png", startx, starty)

class PlayerTeleport(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Purple.png", startx, starty)

class Lava(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Deathbox.png", startx, starty)


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


    for bx in range(35, 1100, 70):
        boxes.add(Box(bx, -105))

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
    boxes.add(Box(35, 450))
    boxes.add(Box(315, 450))
    boxes.add(Box(385, 450))

    # тест ЛАВАшки
    lava = Lava(105, 450)
    lava1 = Lava(175, 450)
    lava2 = Lava(245, 450)
    lava3 = Lava(405, 105)
    lava4 = Lava(405, 104)
    teleport = Teleport(450, 900)
    playerteleport = PlayerTeleport(870, 300)
    usefulteleport = UsefulTeleport(950, 590)








    while True:
        pygame.event.pump()
        player.update(boxes)

        # Draw loop
        screen.blit(bg, (0, 0))
        player.draw(screen)
        boxes.draw(screen)
        lava.draw(screen)
        lava1.draw(screen)
        lava2.draw(screen)
        lava3.draw(screen)
        lava4.draw(screen)
        teleport.draw(screen)
        usefulteleport.draw(screen)
        playerteleport.draw(screen)

        if pygame.sprite.collide_rect(player, usefulteleport):
            while player.move(), list(len(0, 10000))):
                boxes.add(Box(470, 500))
                usefulteleport = UsefulTeleport(10000, 10000)

        if pygame.sprite.collide_rect(player, lava4):
            player.move(500, 500, boxes)

        if pygame.sprite.collide_rect(player, playerteleport):
            player.move(0, -380, boxes)

        if pygame.sprite.collide_rect(player, lava):
            player.move(800, 550, boxes)

        if pygame.sprite.collide_rect(player, lava1):
            player.move(800, 550, boxes)

        if pygame.sprite.collide_rect(player, lava2):
            player.move(800, 550, boxes)

        if pygame.sprite.collide_rect(player, teleport):
            boxes.add(Box(500, 500))
            teleport = Teleport(10000, 10000)
        pygame.display.flip()

        clock.tick(60)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()


if __name__ == "__main__":
    main()