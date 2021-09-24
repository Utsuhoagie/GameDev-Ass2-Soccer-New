import pygame as pg
import pymunk as pm
import math as mth
import os
import random
from typing import *

from pymunk.vec2d import Vec2d
from Assets.Assets import *

pg.init()

# ----- Window --------------------------------------

WIDTH, HEIGHT = BG_W,BG_H

border = 20
midX, midY = WIDTH/2, HEIGHT/2

thickness = 1

screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Tiny football")

space = pm.Space()
# space.gravity = 0,0



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

# ----- Fonts ---------------------------------------

MAIN_FONT = pg.font.SysFont("arial",12)

# ----- Audio ---------------------------------------



# ----- Gameplay ------------------------------------
FPS = 60

MAX_STAMINA = 50
HEAL_STAMINA = 2
SPEND_STAMINA = 4

P_SPEED = 220
P_SPEED_MULTIPLIER = 3

B_VEL = (-100,100)
B_VEL_UPPER_LIMIT = 1100
B_VEL_LOWER_LIMIT = 50
B_ANIM_SPEED = 0.0006
FRICTION = 0.997

# ----- Functions -----------------------------------

# def convertPos(pos: tuple) -> tuple:
#     return pos
#     return (pos[0], HEIGHT - pos[1])

# ----- Classes -------------------------------------

class Wall:
    def __init__(self, pointA, pointB, id, color = None):
        self.body = pm.Body(body_type = pm.Body.STATIC)

        self.shape = pm.Segment(self.body, pointA, pointB, thickness)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = 0
        self.shape.id = id


        if color is not None:
            self.color = color
        else:
            self.color = WHITE

        space.add(self.body, self.shape)

    def draw(self):
        pass
        # a = self.shape.a
        # b = self.shape.b
        
        #pg.draw.line(screen, self.color, a, b, int(self.shape.radius))


class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, vel: tuple):
        # pass in (x,y) in pm.Space <=> (0,0) is bottom left

        self.body = pm.Body()
        self.body.position = x,y
        self.body.mass = 50
        self.body.velocity = vel

        self.shape = pm.Circle(self.body, BALL_R)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = 1

        self.frames = BALL
        self.maxFrames = len(self.frames)
        self.animIndex = 0
        self.animating = False
        self.image = self.frames[0]
        self.ogImage = self.frames[0]


        space.add(self.body, self.shape)

    def update(self):
        #self.body.velocity
        if self.body.velocity.length > B_VEL_UPPER_LIMIT:
            self.body.velocity = self.body.velocity.scale_to_length(B_VEL_UPPER_LIMIT)
        elif self.body.velocity.length < B_VEL_LOWER_LIMIT:
            self.body.velocity = 0,0

        if self.body.velocity.length == 0:
            self.animating = False
        else:
            self.animating = True

    def draw(self):
        blitPos = self.body.position[0] - self.shape.radius, self.body.position[1] - self.shape.radius
        
        if 1 < round(self.body.angle) % 10 < 9:
            # fix blitPos slightly, if angle is diagonal
            blitPos = blitPos[0] - 8, blitPos[1] - 8

        if self.animating:
            self.image = self.frames[int(self.animIndex)]
            self.animIndex = self.animIndex + B_ANIM_SPEED * (self.body.velocity.length * mth.log(self.body.velocity.length, 100))
            if self.animIndex >= self.maxFrames - 1:
                self.animIndex = 0
        
        # blit in pg.Surface <=> (0,0) is top left
        # print("pm.Space() pos = " + str((x,y)))
        # print(str(self.body.velocity) + "  |  " + str(self.body.velocity.length))
        self.body.angle = self.body.velocity.get_angle_degrees_between(Vec2d(1,0))
        # print(self.body.angle)
        
        self.image = pg.transform.rotozoom(self.frames[int(self.animIndex)], self.body.angle, 1)

        self.body.velocity *= FRICTION
        #pg.draw.circle(screen, RED, self.body.position, self.shape.radius)
        screen.blit(self.image, blitPos)



class Player(pg.sprite.Sprite):
    def __init__(self, x, y, id: int):
        self.body = pm.Body(body_type = pm.Body.KINEMATIC)
        self.body.position = x, y

        self.shape = pm.Circle(self.body, P1_R)
        self.shape.elasticity = 1
        self.shape.collision_type = 2

        self.frames = [P1, P1_CHARGE]

        self.image = self.frames[0]
        self.ogImage = self.frames[0]
        self.angle = mth.degrees(self.body.angle)

        self.touchL = False
        self.touchR = False
        self.touchU = False
        self.touchD = False

        self.fast = False
        self.heldFast = False
        self.stamina = MAX_STAMINA

        space.add(self.body, self.shape)

    def update(self):
        # if self.fast and (self.stamina > 0):
        #     self.stamina -= 1
        # else:
        #     self.fast = False
        #     if self.stamina < 10:
        #         self.stamina += 1
        if not self.heldFast and not self.fast and self.stamina < MAX_STAMINA:
            self.stamina += HEAL_STAMINA


    def draw(self):
        if self.fast and self.body.velocity.length > 0:
            self.image = self.frames[1]
            self.ogImage = self.frames[1]
        else:
            self.image = self.frames[0]
            self.ogImage = self.frames[0]

        self.image = pg.transform.rotate(self.ogImage, self.angle)
        blitPos = self.body.position[0] - self.image.get_width()//2, self.body.position[1] - self.image.get_height()//2
        #self.angle = mth.degrees(self.body.angle)
        #print(self.angle)

        screen.blit(self.image, blitPos)

        #pg.draw.circle(screen, RED, self.body.position, 2)


# ----- Main game functions ---------------------

def handleInput(player: Player):

    pVel = player.body.velocity
    keys = pg.key.get_pressed()

    dir = ""

    if keys[pg.K_LEFT]:
        dir += "L"
    if keys[pg.K_RIGHT]:
        dir += "R"
    if keys[pg.K_UP]:
        dir += "U"
    if keys[pg.K_DOWN]:
        dir += "D"


    if dir in ["L","LUD"]:
        player.body.angle = mth.radians(-180)
        player.angle = -180
        if not player.touchL:
            pVel = -P_SPEED,0
        else:
            pVel = 0,0

    if dir in ["R","RUD"]:
        player.body.angle = mth.radians(0)
        player.angle = 0
        if not player.touchR:
            pVel = P_SPEED,0
        else:
            pVel = 0,0

    if dir in ["U","LRU"]:
        player.body.angle = mth.radians(90)
        player.angle = 90
        if not player.touchU:
            pVel = 0,-P_SPEED
        else:
            pVel = 0,0

    if dir in ["D","LRD"]:
        player.body.angle = mth.radians(-90)
        player.angle = -90
        if not player.touchD:
            pVel = 0,P_SPEED
        else:
            pVel = 0,0

    if dir == "LU":
        player.body.angle = mth.radians(135)
        player.angle = 135
        if (not player.touchL) and (not player.touchU):
            pVel = -P_SPEED,-P_SPEED
        elif not player.touchL:
            pVel = -P_SPEED,0
        elif not player.touchU:
            pVel = 0,-P_SPEED
        else:
            pVel = 0,0

    if dir == "LD":
        player.body.angle = mth.radians(-135)
        player.angle = -135
        if (not player.touchL) and (not player.touchD):
            pVel = -P_SPEED,P_SPEED
        elif not player.touchL:
            pVel = -P_SPEED,0
        elif not player.touchD:
            pVel = 0,P_SPEED
        else:
            pVel = 0,0

    if dir == "RU":
        player.body.angle = mth.radians(45)
        player.angle = 45
        if (not player.touchR) and (not player.touchU):
            pVel = P_SPEED,-P_SPEED
        elif not player.touchR:
            pVel = P_SPEED,0
        elif not player.touchU:
            pVel = 0,-P_SPEED
        else:
            pVel = 0,0

    if dir == "RD":
        player.body.angle = mth.radians(-45)
        player.angle = -45
        if (not player.touchR) and (not player.touchD):
            pVel = P_SPEED,P_SPEED
        elif not player.touchR:
            pVel = P_SPEED,0
        elif not player.touchD:
            pVel = 0,P_SPEED
        else:
            pVel = 0,0

    if dir in ["","LR","UD","LRUD"]:
        pVel = 0,0


    if keys[pg.K_SPACE] and (player.stamina >= 0):
        player.fast = True
        player.heldFast = True
    else:
        if not keys[pg.K_SPACE]:
            player.heldFast = False
        player.fast = False

    if player.fast:
        pVel = pVel[0] * P_SPEED_MULTIPLIER, pVel[1] * P_SPEED_MULTIPLIER
        player.stamina -= SPEND_STAMINA

    #print(str(pVel) + "  |  " + str(Vec2d(pVel[0],pVel[1]).length) + "  |  stamina = " + str(player.stamina) + "  |  fast = " + str(player.fast))

    player.body.velocity = pVel


def update():
    p1.update()
    ball.update()

def draw():
    screen.fill(BLACK)
    screen.blit(BG,(0,0))

    ball.draw()

    p1.draw()

    for wall in wallList:
        wall.draw()
    #self.wallGroup.draw()

    pg.display.update()


# ----- CollisionHandler functions -----------------------

def beginTouchWall(arbiter, space, data) -> bool:
    #print("Collided and handled!")

    wall = arbiter.shapes[1].id
    
    if wall == 1:
        p1.touchL = True
    elif wall == 2:
        p1.touchR = True
    elif wall == 3:
        p1.touchU = True
    elif wall == 4:
        p1.touchD = True

    return True

def separateTouchWall(arbiter, space, data):
    wall = arbiter.shapes[1].id

    if wall == 1:
        p1.touchL = False
    elif wall == 2:
        p1.touchR = False
    elif wall == 3:
        p1.touchU = False
    elif wall == 4:
        p1.touchD = False


# +====================================================================+
# || ACTUAL GAME                                                      ||
# +====================================================================+

# NOTE: Passing in (x,y) coordinates in pm.Space() <=> (0,0) is bottom left
# So Pymunk's physics are upside down, but Pygame still blits it correctly

vel = B_VEL
ball = Ball(midX, 80, vel)

p1 = Player(150, 240, 11)

wallL = Wall((border, border), (border, HEIGHT - border), 1)
wallR = Wall((WIDTH - border, border), (WIDTH - border, HEIGHT - border), 2)
wallU = Wall((border, border), (WIDTH - border, border), 3)
wallD = Wall((border, HEIGHT - border), (WIDTH - border, HEIGHT - border), 4)

wallList = [wallL, wallR, wallU, wallD]
#self.wallGroup = pg.sprite.Group(self.wallL, self.wallR, self.wallU, self.wallD)


def main():
    run = True
    clock = pg.time.Clock()
    handler_P1_Wall = space.add_collision_handler(2, 0)
    handler_P1_Wall.begin = beginTouchWall
    handler_P1_Wall.separate = separateTouchWall

    # handler_P1_Ball = space.add_collision_handler(2, 1)
    # handler_P1_Ball.begin = beginTouchBall
    # handler_P1_Ball.post_solve = postSolveTouchBall

    while run:
        space.step(1/FPS)
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run = False
                break
            if event.type == pg.KEYUP and (event.key == pg.K_SPACE):
                p1.fast = True

        handleInput(p1)
        update()

        draw()

    pg.quit()



if __name__ == '__main__':
    main()