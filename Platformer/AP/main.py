import pygame
import numpy
import random
import time

c = 0
w = 0
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
        super().__init__("LavaAlt (2).png", startx, starty, )

class Ball(Sprite):
    def __init__(self, startx, starty):
        super().__init__("фиол-краска.png", startx, starty, )

class Platforma(Sprite):
    def __init__(self, startx, starty):
        super().__init__("teleport.png", startx, starty, )





def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

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

    lava = Lava(140, 415)
    lava1 = Lava(631, 720)
    lava2 = Lava(700, 720)
    lava3 = Lava(770, 720)
    lava4 = Lava(421, 1000)
    lava5 = Lava(491, 1000)
    lava6 = Lava(561, 1000)
    lava7 = Lava(140, 1000)

    ball = Ball(1050, 680)
    ball2 = Ball(100, 950)
    win = Platforma(1049, 955)



    # лестница
    for bx in range(280, 350, 70):
        boxes.add(Box(bx, 930))
    for bx in range(280, 350, 70):
        boxes.add(Box(bx, 860))
    for bx in range(139, 140, 70):
        boxes.add(Box(bx, 480))
    for bx in range(69, 70, 70):
        boxes.add(Box(bx, 410))

    global c
    global w
    while True and c != 3 and w != 1:
        pygame.event.pump()
        player.update(boxes)

        # Draw loop
        player.draw(screen)
        boxes.draw(screen)

        lava.draw(screen)
        if pygame.sprite.collide_rect(player, lava):
            player.move(-100, -200, boxes)
            c=c+1

        lava1.draw(screen)
        if pygame.sprite.collide_rect(player, lava1):
            player.move(-650, -250, boxes)
            c=c+1

        lava2.draw(screen)
        if pygame.sprite.collide_rect(player, lava2):
            player.move(-720, -250, boxes)
            c = c + 1

        lava3.draw(screen)
        if pygame.sprite.collide_rect(player, lava3):
            player.move(-790, -250, boxes)
            c = c + 1

        lava4.draw(screen)
        if pygame.sprite.collide_rect(player, lava4):
            player.move(-580, -900, boxes)
            c = c + 1

        lava5.draw(screen)
        if pygame.sprite.collide_rect(player, lava5):
            player.move(-510, -900, boxes)
            c = c + 1

        lava6.draw(screen)
        if pygame.sprite.collide_rect(player, lava6):
            player.move(-440, -900, boxes)
            c = c + 1

        lava7.draw(screen)
        if pygame.sprite.collide_rect(player, lava7):
            player.move(-100, -900, boxes)
            c = c + 1

        ball.draw(screen)
        if pygame.sprite.collide_rect(player, ball):
            player.move(-800, 400, boxes)

        ball2.draw(screen)
        if pygame.sprite.collide_rect(player, ball2):
            player.move(800, 100, boxes)

        win.draw(screen)
        if pygame.sprite.collide_rect(player, win):
            player.move(0, 0, boxes)
            w = w + 1

        pygame.display.flip()
        screen.blit(bg, (0, 0))
        clock.tick(60)





if __name__ == "__main__":
    main()
