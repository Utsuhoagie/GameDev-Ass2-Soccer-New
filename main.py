import pygame as pg
import pymunk as pm
import pymunk.pygame_util
import math as mth
import os
import random
from typing import *

from pymunk.vec2d import Vec2d
from Assets.Assets import *
from Constants import *

pg.init()

# ----- Window --------------------------------------

# MENU_HEIGHT = 80

# WIDTH, HEIGHT = BG_W, BG_H + MENU_HEIGHT

# BORDER = 20
# MIDX, MIDY = BG_W/2, BG_H/2 + MENU_HEIGHT

# THICKNESS = 7

screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Tiny football")

space = pm.Space()



# ----- Colors --------------------------------------

# BLACK = (0,0,0)
# GRAY = (100,100,100)
# WHITE = (255,255,255)

# RED = (255,0,0)
# GREEN = (0,255,0)
# BLUE = (0,0,255)
# YELLOW = (252,227,0)
# BROWN = (115,67,38)
# LIGHTGREEN = (102,199,28)

# ----- Fonts ---------------------------------------


# ----- Audio ---------------------------------------



# ----- Gameplay ------------------------------------
# FPS = 5

# MAX_STAMINA = 50
# HEAL_STAMINA = 2
# SPEND_STAMINA = 4

# P_SPEED = 220 - 100
# P_SPEED_MULTIPLIER = 4

# B_VEL = (-0,1)
# B_VEL_UPPER_LIMIT = 1000
# B_VEL_LOWER_LIMIT = 50
# B_ANIM_SPEED = 0.0006
# B_FRICTION = 0.997

# COL_WALL = 0
# COL_BALL = 1
# COL_PLAYER = 2
# COL_GOAL = 3

# ----- Functions -----------------------------------

# def convertPos(pos: tuple) -> tuple:
#     return pos
#     return (pos[0], HEIGHT - pos[1])

# ----- Classes -------------------------------------

class Wall:
    def __init__(self, pointA, pointB, id, color = None):
        self.body = pm.Body(body_type = pm.Body.STATIC)

        self.shape = pm.Segment(self.body, pointA, pointB, THICKNESS)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = COL_WALL
        self.shape.id = id

        space.add(self.body, self.shape)

    def draw(self):
        pg.draw.line(screen, BLUE, self.shape.a, self.shape.b, 5)


class Goal(pg.sprite.Sprite):
    def __init__(self, pointA, pointB, id: int):
        super().__init__()
        self.body = pm.Body(body_type = pm.Body.STATIC)

        self.shape = pm.Segment(self.body, pointA, pointB, 2)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = COL_GOAL
        #self.shape.sensor = True
        self.shape.id = id

        space.add(self.body, self.shape)

    def draw(self):
        pg.draw.line(screen, RED, self.shape.a, self.shape.b, 5)


class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, vel: tuple):
        # pass in (x,y) in pm.Space <=> (0,0) is bottom left
        super().__init__()
        self.body = pm.Body()
        self.body.position = x,y
        self.body.mass = 1
        self.body.velocity = vel

        self.shape = pm.Circle(self.body, BALL_R)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = COL_BALL
        self.shape.touchedGoal = False

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

        self.body.velocity *= B_FRICTION
        #pg.draw.circle(screen, RED, self.body.position, self.shape.radius)
        screen.blit(self.image, blitPos)



class Player(pg.sprite.Sprite):
    score = 0
    def __init__(self, x, y, id: int):
        super().__init__()
        self.body = pm.Body(body_type = pm.Body.KINEMATIC)
        self.body.position = x, y

        self.shape = pm.Circle(self.body, P1_R)
        self.shape.elasticity = 1
        self.shape.collision_type = COL_PLAYER

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

        #self.image = pg.transform.rotate(self.ogImage, self.angle)
        blitPos = self.body.position[0] - self.image.get_width()//2, self.body.position[1] - self.image.get_height()//2
        #self.angle = mth.degrees(self.body.angle)
        #print(self.angle)

        screen.blit(self.image, blitPos)

        #pg.draw.circle(screen, RED, self.body.position, 2)

class ScoreController:
    def __init__(self):
        self.score_P1 = 0
        self.score_P2 = 0
    
    def draw(self):
        scoreSurf = FONT.render("Score P1 = " + str(self.score_P1) + "Score P2 = " + str(self.score_P2), 1, BLUE)
        screen.blit(scoreSurf, (MIDX - scoreSurf.get_width()//2, 20))


class Timer:
    def __init__(self):
        self.timer = 0

    def set(self, n: int):
        self.timer = n

    def timeUp(self) -> bool:
        return self.timer == 0

    def update(self):
        if self.timer:
            self.timer -= 1
        elif self.timer == 0 and ball.shape.touchedGoal:
            resetBall()

    


# ----- CollisionHandler functions ---------------------------------------------------

def begin_PlayerWall(arbiter, space, data) -> bool:
    #print("Collided and handled!")

    wall = arbiter.shapes[1].id

    for player in p1Group:    
        if wall == 1:
            player.touchL = True
        elif wall == 2:
            player.touchR = True
        elif wall == 3:
            player.touchU = True
        elif wall == 4:
            player.touchD = True

    return True

def separate_PlayerWall(arbiter, space, data):
    wall = arbiter.shapes[1].id

    for player in p1Group:
        if wall == 1:
            player.touchL = False
        elif wall == 2:
            player.touchR = False
        elif wall == 3:
            player.touchU = False
        elif wall == 4:
            player.touchD = False


def begin_BallGoal(arbiter, space, data) -> bool:
    
    #space.bodies.ball.velocity = space.bodies.ball.velocity.scale_to_length(100)
    
    #arbiter.shapes[0].body.velocity = arbiter.shapes[0].body.velocity.scale_to_length(80)
    
    # arbiter.shapes[0].collision_type = COL_WALL
    # arbiter.shapes[1].collision_type = COL_WALL


    arbiter.shapes[0].touchedGoal = True
    
    
    arbiter.shapes[0].body.velocity = arbiter.shapes[0].body.velocity.scale_to_length(55)
    # print(arbiter.shapes[0].body.velocity)
    # arbiter.shapes[0].body.velocity = abs(arbiter.shapes[0].body.velocity[0]), arbiter.shapes[0].body.velocity[1]

    if arbiter.shapes[1].id == 1:
        score.score_P2 += 1
    else:
        score.score_P1 += 1
    
    timer.set(90) # pause for 1.5s

                # for i in range(0,5000):
                #     pass

                # ball.body.position = MIDX, MIDY
                # ball.body.velocity = 0,0
                # ball.shape.touchedGoal = False



    # print("aaaaaa" + str(arbiter.shapes[0].collision_type))

    

    # for i in range(0,6):
    #     arbiter.shapes[0].body.velocity = 0, 0
    #     arbiter.shapes[0].body.position = arbiter.shapes[0].body.position[0] + (6 - i), arbiter.shapes[0].body.position[1]


    return False

def postSolve_BallGoal(arbiter, space, data):
    
    

    #txtSurf = MAIN_FONT.render("Goal!", 1, BLUE)
    # otherFont = pg.font.SysFont("arial", 100)
    # txtSurf = otherFont.render("Goal!!!", 1, BLUE)
    # screen.blit(txtSurf, (0,0))
    # screen.blit(txtSurf, (MIDX - txtSurf.get_width()//2, MIDY - txtSurf.get_height()//2))
    #print((MIDX - txtSurf.get_width()//2, MIDY - txtSurf.get_height()//2))
    #pg.time.delay(800)


    pass
    
def begin_BallWall(arbiter, space, data) -> bool:
    print("here")
    print(arbiter.shapes[0].touchedGoal)
    if arbiter.shapes[0].touchedGoal:
        #arbiter.shapes[0].body.velocity = arbiter.shapes[0].body.velocity.scale_to_length(51)
        #arbiter.shapes[0] = pm.Circle(arbiter.shapes[0].body, 1)
        #print(type(arbiter.shapes[0]))
        return False
    else:
        return True

def begin_BallPlayer(arbiter, space, data) -> bool:
    if arbiter.shapes[0].touchedGoal:
        #arbiter.shapes[0].body.velocity = arbiter.shapes[0].body.velocity.scale_to_length(55)
        #arbiter.shapes[0] = pm.Circle(arbiter.shapes[0].body, 1)
        #print(type(arbiter.shapes[0]))
        return False
    else:
        return True



# ----- Main game functions ---------------------

def resetBall():
    ball.body.position = MIDX, MIDY
    ball.body.velocity = random.randint(-300,300), random.randint(-300,300)
    if ball.body.velocity.length <= 100:
        ball.body.velocity = ball.body.velocity.scale_to_length(200)

    ball.shape.touchedGoal = False

def handleInput(player: Player):

    pVel = player.body.velocity
    keys = pg.key.get_pressed()

    dir = ""

    if keys[pg.K_LEFT]:
        #dir += "L"
        pass
    if keys[pg.K_RIGHT]:
        #dir += "R"
        pass
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
    p1Group.update()
    ball.update()
    timer.update()

def draw():
    screen.fill(GREEN)
    screen.blit(BG, (0,80))

    ball.draw()

    #p1Group.draw(screen)
    for sprite in p1Group.sprites():
        sprite.draw()

    for goal in goalGroup.sprites():
        goal.draw()

    for wall in wallList:
        wall.draw()

    score.draw()

    # print(ball.body.velocity)

    pg.display.update()




# +====================================================================+
# || ACTUAL GAME                                                      ||
# +====================================================================+


# NOTE: Passing in (x,y) coordinates in pm.Space() <=> (0,0) is bottom left
# So Pymunk's physics are upside down, but Pygame still blits it correctly

vel = B_VEL
ball = Ball(MIDX, MIDY, vel)

score = ScoreController()

p1 = Player(150, MIDY, 11)
p2 = Player(150, MIDY - 50, 11)
#p3 = Player(350, 240, 11)
#pG = Player(450, 240, 11)

wallL = Wall((BORDER, BORDER + MENU_HEIGHT), (BORDER, HEIGHT - BORDER), 1)
wallR = Wall((WIDTH - BORDER, BORDER + MENU_HEIGHT), (WIDTH - BORDER, HEIGHT - BORDER), 2)
wallU = Wall((BORDER, BORDER + MENU_HEIGHT), (WIDTH - BORDER, BORDER + MENU_HEIGHT), 3)
wallD = Wall((BORDER, HEIGHT - BORDER), (WIDTH - BORDER, HEIGHT - BORDER), 4)

goal1 = Goal((BORDER + 5, MIDY - 80), (BORDER + 5, MIDY + 80), 1)
goal2 = Goal((WIDTH - BORDER - 5, MIDY - 80), (WIDTH - BORDER - 5, MIDY + 80), 2)


p1Group = pg.sprite.Group(p1, p2)   #,p2,p3,pG)
goalGroup = pg.sprite.Group(goal1, goal2)
#goalList = [goalL, goalR]
wallList = [wallL, wallR, wallU, wallD]
#self.wallGroup = pg.sprite.Group(self.wallL, self.wallR, self.wallU, self.wallD)

#debugOptions = pm.pygame_util.DrawOptions(screen)
timer = Timer()

def main():
    run = True
    clock = pg.time.Clock()
    handler_P_Wall = space.add_collision_handler(COL_PLAYER, COL_WALL)
    handler_P_Wall.begin = begin_PlayerWall
    handler_P_Wall.separate = separate_PlayerWall


    handler_Ball_Goal = space.add_collision_handler(COL_BALL, COL_GOAL)
    handler_Ball_Goal.begin = begin_BallGoal
    handler_Ball_Goal.post_solve = postSolve_BallGoal

    handler_Ball_Wall = space.add_collision_handler(COL_BALL, COL_WALL)
    handler_Ball_Wall.begin = begin_BallWall

    handler_Ball_Player = space.add_collision_handler(COL_BALL, COL_PLAYER)
    handler_Ball_Player.begin = begin_BallPlayer



    while run:
        space.step(1/FPS)
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run = False
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                resetBall()
            if event.type == pg.KEYUP and event.key == pg.K_SPACE:
                for player in p1Group:
                    player.fast = True
            

        for sprite in p1Group.sprites():
            handleInput(sprite)

        update()

        draw()


    pg.quit()



if __name__ == '__main__':
    main()