import pygame as pg
import os
pg.init()

# ----- Fonts ----------------------

FONT = pg.font.SysFont("consolas", 48)
TITLE_FONT = pg.font.Font(os.path.join("Assets","SF Atarian System.ttf"), 72)
BUTTON_FONT = pg.font.Font(os.path.join("Assets","SF Atarian System.ttf"), 50)

# ----- Audio ----------------------
BOUNCE = pg.mixer.Sound(os.path.join("Assets","Sounds","bounce.ogg"))

# ----- Sprites --------------------

# Background
BG = pg.image.load(os.path.join("Assets","bg.png"))
BG_W = BG.get_width()
BG_H = BG.get_height()

MENU_BG = pg.image.load(os.path.join("Assets","menu_bg.png"))


# Ball
BALL_1 = pg.image.load(os.path.join("Assets","Sprites","Ball","b1.png"))
BALL_2 = pg.image.load(os.path.join("Assets","Sprites","Ball","b2.png"))
BALL_3 = pg.image.load(os.path.join("Assets","Sprites","Ball","b3.png"))
BALL_4 = pg.image.load(os.path.join("Assets","Sprites","Ball","b4.png"))
BALL_5 = pg.image.load(os.path.join("Assets","Sprites","Ball","b5.png"))
BALL_6 = pg.image.load(os.path.join("Assets","Sprites","Ball","b6.png"))

BALL = [BALL_1, BALL_2, BALL_3, BALL_4, BALL_5, BALL_6]

BALL_R = BALL_1.get_width()//2


# Players
P1 = pg.image.load(os.path.join("Assets","Sprites","Players","blue.png"))
P1_R = P1.get_width()//2

P2 = pg.image.load(os.path.join("Assets","Sprites","Players","red.png"))
P2 = pg.transform.flip(P2, 1, 0)
P2_R = P1.get_width()//2