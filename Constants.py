from Assets.Assets import *

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
COL_PLAYER1 = 2
COL_PLAYER2 = 3
COL_GOAL = 4

GROUP_WALL = 1
GROUP_BALL = 2