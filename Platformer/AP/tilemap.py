import pygame as pg
import constants

BOX = 0
WATER = 1




textures = {
    BOX : pg.image.load("image\\boxAlt.png"),
    WATER : pg.image.load("image\\boxAlt.png")

    }


tilemap = [
    [BOX, BOX, BOX, BOX],
    [BOX, BOX, BOX, BOX],
    [BOX, BOX, BOX, BOX],
    [BOX, BOX, BOX, BOX]    
    ]



tilesize = 40
mapwidth = 2
mapheight = 5