import keyboard
import pygame
from pygame.locals import *
import pygame as pg
import numpy
import sys
import pygame_menu
import random
import time

c = 0
pygame.init()

WIDTH = 1090
HEIGHT = 1020
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


class invTeleport(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)


class Finish(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Finish.png", startx, starty)


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
        boxes.add(Box(bx, 985))

    for bx in range(35, 1100, 70):
        boxes.add(Box(1150, bx))

    for bx in range(35, 1100, 70):
        boxes.add(Box(-35, bx))

    boxes.add(Box(1035, 175))  # \
    boxes.add(Box(1035, 245))  # Лестница
    boxes.add(Box(1035, 315))  # /
    boxes.add(Box(1035, 385))  # /
    boxes.add(Box(1055, 650))  # \\
    boxes.add(Box(985, 650))  # \
    boxes.add(Box(915, 650))  # \
     # Правая нижняя платформа
    boxes.add(Box(775, 650))  # /
    boxes.add(Box(705, 650))  # /
    boxes.add(Box(635, 650))
    boxes.add(Box(1035, 385))  # \
    boxes.add(Box(965, 385))  # Правая верхняя платформа
    boxes.add(Box(895, 385))
    boxes.add(Box(825, 385))
    boxes.add(Box(35, 450))
    boxes.add(Box(315, 450))
    boxes.add(Box(385, 450))
    boxes.add(Box(335, 105))
    boxes.add(Box(265, 105))
    boxes.add(Box(195, 105))
    boxes.add(Box(125, 105))
    boxes.add(Box(55, 105))
    boxes.add(Box(-15, 105))
    boxes.add(Box(475, 105))
    boxes.add(Box(545, 105))
    boxes.add(Box(615, 105))
    boxes.add(Box(685, 105))
    boxes.add(Box(755, 105))
    boxes.add(Box(825, 105))
    boxes.add(Box(895, 105))
    boxes.add(Box(965, 105))
    boxes.add(Box(1035, 105))
    boxes.add(Box(1105, 105))

    # тест ЛАВЮшки
    lava = Lava(105, 450)
    lava1 = Lava(175, 450)
    lava2 = Lava(245, 450)
    lava3 = Lava(405, 105)
    lava5 = Lava(175, 985)
    lava6 = Lava(845, 650)
    lava7 = Lava(175, 984)
    teleport = Teleport(450, 900)
    finish = Finish(55, 62)
    playerteleport = PlayerTeleport(870, 300)
    usefulteleport = UsefulTeleport(950, 590)
    usefulteleport1 = UsefulTeleport(10000, 10000)
    invteleport = invTeleport(10000, 10000)
    invteleport1 = invTeleport(10000, 10000)

    global c
    while True and c != 3:

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
        lava5.draw(screen)
        lava6.draw(screen)
        lava7.draw(screen)
        teleport.draw(screen)
        usefulteleport.draw(screen)
        finish.draw(screen)

        playerteleport.draw(screen)

        if pygame.sprite.collide_rect(player, usefulteleport):
            boxes.add(Box(500, 500))
            usefulteleport = UsefulTeleport(10000, 10000)
            usefulteleport1 = UsefulTeleport(485, 735)
            usefulteleport1.draw(screen)
            invteleport.draw(screen)
            invteleport1.draw(screen)
            invteleport = invTeleport(-34, 380)
            invteleport1 = invTeleport(-34, 735)
            teleport = Teleport(10000, 10000)

        usefulteleport1.draw(screen)
        invteleport.draw(screen)
        invteleport1.draw(screen)

        if pygame.sprite.collide_rect(player, usefulteleport1):
            boxes.add(Box(600, 400))
            usefulteleport1 = UsefulTeleport(10000, 10000)

        if pygame.sprite.collide_rect(player, invteleport):
            player.move(100, 400, boxes)

        if pygame.sprite.collide_rect(player, invteleport1):
            player.move(100, -600, boxes)

        if pygame.sprite.collide_rect(player, lava7):
            player = Player(950, 880)
            c = c + 1

        if pygame.sprite.collide_rect(player, finish):
            pygame.quit()

        if pygame.sprite.collide_rect(player, lava3):
            player = Player(950, 880)
            c = c + 1

        if pygame.sprite.collide_rect(player, lava6):
            player = Player(950, 880)
            c = c + 1

        if pygame.sprite.collide_rect(player, playerteleport):
            player.move(0, -380, boxes)

        if pygame.sprite.collide_rect(player, lava):
            player = Player(950, 880)
            c = c + 1

        if pygame.sprite.collide_rect(player, lava1):
            player = Player(950, 880)
            c = c + 1

        if pygame.sprite.collide_rect(player, lava2):
            player = Player(950, 880)
            c = c + 1

        if pygame.sprite.collide_rect(player, lava5):
            player = Player(950, 880)
            c = c + 1

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
