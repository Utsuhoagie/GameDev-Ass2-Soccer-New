from Assets.Assets import *
from enum import Enum
import pygame as pg

MENU_HEIGHT = 80

WIDTH, HEIGHT = BG_W, BG_H + MENU_HEIGHT

BORDER = 20
MIDX, MIDY = BG_W/2, BG_H/2 + MENU_HEIGHT

THICKNESS = 7

# ----- Colors --------------------------------------

BLACK = (0,0,0)
GRAY = (100,100,100)
WHITE = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (252,227,0)
BROWN = (115,67,38)
LIGHTGREEN = (102,199,28)


# ----- Gameplay ------------------------------------
FPS = 60

EVENT_RESET = pg.USEREVENT + 1

MAX_STAMINA = 50
HEAL_STAMINA = 4
SPEND_STAMINA = 4

P_SPEED = 220
P_SPEED_MULTIPLIER = 3.5

B_VEL = (-350,0)
B_VEL_UPPER_LIMIT = 900
B_VEL_LOWER_LIMIT = 50
B_ANIM_SPEED = 0.0006
B_FRICTION = 0.998

COL_WALL = 0
COL_BALL = 1

COL_PLAYER10 = 10
COL_PLAYER11 = 11
COL_PLAYER12 = 12
COL_PLAYER13 = 13

COL_PLAYER20 = 20
COL_PLAYER21 = 21
COL_PLAYER22 = 22
COL_PLAYER23 = 23

COL_GOAL = 4

GROUP_WALL = 1
GROUP_BALL = 2

# Keys caps

class Player1Keys(int):
    UP = pg.K_a
    DOWN = pg.K_s
    LEFT = pg.K_a
    RIGHT = pg.K_d

class Player2Keys(int):
    UP = pg.K_UP
    DOWN = pg.K_DOWN
    LEFT = pg.K_LEFT
    RIGHT = pg.K_RIGHT