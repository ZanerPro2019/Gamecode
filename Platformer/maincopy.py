from subprocess import call
import keyboard
import pygame
from pygame.locals import *
import pygame as pg
import numpy
import sys
import pygame_menu
import random
import time
import os

pygame.init()
kill = 0
level = 1
WIDTH = 1090
HEIGHT = 1020
BACKGROUND = (0, 0, 0)
bg = pygame.image.load("background.jpg")
win = pygame.display.set_mode((WIDTH,HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



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

        self.walk_cycle = [pygame.image.load(f"anim/p1_walk{i:0>2}.png") for i in range(1, 12)]
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

        if key[pygame.K_a]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_d]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_w] and onground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_w] and not key[pygame.K_w]:
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


class Lava(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Deathbox.png", startx, starty, )

class Ball(Sprite):
    def __init__(self, startx, starty):
        super().__init__("purple.png", startx, starty, )

class Platforma(Sprite):
    def __init__(self, startx, starty):
        super().__init__("teleport.png", startx, starty, )


def help_g():
    help_f = os.system('help.txt')



def main():
    player = Player(100, 200)
    boxes = pygame.sprite.Group()

    
    for bx in range(630, 1100, 70):
        boxes.add(Box(bx, 1000))
    for bx in range(0, 90, 70):
        boxes.add(Box(bx, 1000))
    for bx in range(210, 400, 70):
        boxes.add(Box(bx, 1000))
    for bx in range(0, 980, 70):
        boxes.add(Box(bx, 790))
    for bx in range(420, 600, 70):
        boxes.add(Box(bx, 720))
    for bx in range(840, 1100, 70):
        boxes.add(Box(bx, 720))
    for bx in range(0, 560, 70):
        boxes.add(Box(bx, 550))
    for bx in range(0, 80, 70):
        boxes.add(Box(bx, 340))
    for bx in range(310, 1150, 70):
        boxes.add(Box(bx, 290))
    for bx in range(1050, 1120, 70):
        boxes.add(Box(bx, 220))
    for bx in range(1050, 1120, 70):
        boxes.add(Box(bx, 150))
    for bx in range(0, 1120, 70):
        boxes.add(Box(bx, 80))
    for bx in range(69, 70, 70):
        boxes.add(Box(bx, 480))
    for bx in range(280, 350, 70):
        boxes.add(Box(bx, 930))
    for bx in range(280, 350, 70):
        boxes.add(Box(bx, 860))
    for bx in range(139, 140, 70):
        boxes.add(Box(bx, 480))
    for bx in range(69, 70, 70):
        boxes.add(Box(bx, 410))

    lava = Lava(139, 415)
    lava1 = Lava(630, 720)
    lava2 = Lava(700, 720)
    lava3 = Lava(770, 720)
    lava4 = Lava(420, 1000)
    lava5 = Lava(490, 1000)
    lava6 = Lava(560, 1000)
    lava7 = Lava(140, 1000)

    ball = Ball(1050, 680)
    ball1 = Ball(100, 950)
    checkpoint = Platforma(1049, 955)




    global kill
    global level
    while True:
        if kill != 3:
            if player .rect.bottom > 1100:
                player.kill()
                player = Player (100, 200)
                kill += 1
            lava_list = [lava, lava1, lava2, lava3, lava4, lava5, lava6, lava7]
            for current_lava in lava_list:
                if pygame.sprite.collide_rect(player, current_lava):
                    player.move(-100, -250, boxes)
                    kill += 1
            if pygame.sprite.collide_rect(player, ball):
                player.move(-800, 400, boxes)
            if pygame.sprite.collide_rect(player, ball1):
                player.move(800, 100, boxes)
            if pygame.sprite.collide_rect(player, checkpoint):
                
                player.move(0, 0, boxes)
                level += 1
                print('lvl done', level)
                checkpoint.image = pygame.image.load('teleport_pushed.png')
            else:
                checkpoint.image = pygame.image.load('teleport.png')



            
                
            pygame.event.pump()
            player.update(boxes)

            # Draw loop
            screen.blit(bg, (0, 0))
            player.draw(screen)
            boxes.draw(screen)
            ball.draw(screen)
            ball1.draw(screen)
            lava.draw(screen)
            lava1.draw(screen)
            lava2.draw(screen)
            lava3.draw(screen)
            lava4.draw(screen)
            lava5.draw(screen)
            lava6.draw(screen)
            lava7.draw(screen)
            checkpoint.draw(screen)
            pygame.display.flip()

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

        elif kill == 3:
            kill = 0
            menu = pygame_menu.Menu('You died', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
    
            menu.add.button('Play again', main)
            menu.add.button('Help', help_g)
            menu.add.button('Quit', pygame_menu.events.EXIT)

            menu.mainloop(win)




if __name__ == "__main__":
    main()

# https://ru.stackoverflow.com/questions/1514430/Оптимизация-циклов
