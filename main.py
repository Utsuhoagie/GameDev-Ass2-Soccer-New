from Objects.Player import *
from Objects.Ball import *
from Objects.Field import *
from Objects.Score import *


# ------ Game global variables -----------------------------

# NOTE: Passing in (x,y) coordinates in pm.Space() <=> (0,0) is bottom left
# So Pymunk's physics are upside down, but Pygame still blits it correctly

ball = Ball(MIDX, MIDY, B_VEL)

score = ScoreController()

p1_1 = Player(200, MIDY + 50, 1)
p1_2 = Player(200, MIDY - 50, 1)

p2_1 = Player(WIDTH - 200, MIDY + 50, 2)
p2_2 = Player(WIDTH - 200, MIDY - 50, 2)


wallL = Wall((BORDER, BORDER + MENU_HEIGHT), (BORDER, HEIGHT - BORDER), 1)
wallR = Wall((WIDTH - BORDER, BORDER + MENU_HEIGHT), (WIDTH - BORDER, HEIGHT - BORDER), 2)
wallU = Wall((BORDER, BORDER + MENU_HEIGHT), (WIDTH - BORDER, BORDER + MENU_HEIGHT), 3)
wallD = Wall((BORDER, HEIGHT - BORDER), (WIDTH - BORDER, HEIGHT - BORDER), 4)

goal1 = Goal((BORDER + 5, MIDY - 80), (BORDER + 5, MIDY + 80), 1)
goal2 = Goal((WIDTH - BORDER - 5, MIDY - 80), (WIDTH - BORDER - 5, MIDY + 80), 2)


pGroup = pg.sprite.Group(p1_1, p1_2, p2_1, p2_2)
goalGroup = pg.sprite.Group(goal1, goal2)
wallList = [wallL, wallR, wallU, wallD]


# ----- Classes -------------------------------------

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
            pg.event.post(pg.event.Event(EVENT_RESET))

timer = Timer()



# ----- CollisionHandler functions ---------------------------------------------------
"""
    When a collision happens, the corresponding pymunk.CollisionHandler for the 2 types of objects will call:
        begin:      before collision happens
                    do calculations/etc
                    returns True if collide (aka bounce off), False if not (aka ignore collision)
                    if returns False, separate() won't be called

        (also call pre_solve, post_solve, but not used here)

        separate:   after 2 objects are separated

    Arbiter: basically contains info about the 2 colliding objects:
        usually use arbiter.shapes to get the shapes of the objects
            or arbiter.shapes[i].body to get the body of the i-th shape (i = 0 or 1)
            etc
        
        check members of the classes in Objects files!!!
"""


def begin_PlayerWall(arbiter, space, data) -> bool:

    wall = arbiter.shapes[1].id
    pid = arbiter.shapes[0].id

    for player in pGroup:    
        if wall == 1 and player.shape.id == pid:
            player.touchL = True
        elif wall == 2 and player.shape.id == pid:
            player.touchR = True
        elif wall == 3 and player.shape.id == pid:
            player.touchU = True
        elif wall == 4 and player.shape.id == pid: 
            player.touchD = True

    return True

def separate_PlayerWall(arbiter, space, data):
    wall = arbiter.shapes[1].id
    pid = arbiter.shapes[0].id

    for player in pGroup:
        if wall == 1 and player.shape.id == pid:
            player.touchL = False
        elif wall == 2 and player.shape.id == pid:
            player.touchR = False
        elif wall == 3 and player.shape.id == pid:
            player.touchU = False
        elif wall == 4 and player.shape.id == pid:
            player.touchD = False


def begin_BallGoal(arbiter, space, data) -> bool:

    arbiter.shapes[0].touchedGoal = True
    arbiter.shapes[0].body.velocity = arbiter.shapes[0].body.velocity.scale_to_length(55)

    if arbiter.shapes[1].id == 1:
        score.score_P2 += 1
    else:
        score.score_P1 += 1
    
    timer.set(90)   # pause for 1.5s

    return False    # no collision

    

# NOTE: These begin functions will make the ball IGNORE all collisions after a goal
#       until it resets (due to begin_BallGoal or pressing 'R')

def begin_BallWall(arbiter, space, data) -> bool:
    if arbiter.shapes[0].touchedGoal:
        return False
    else:
        return True


def begin_BallPlayer(arbiter, space, data) -> bool:
    if arbiter.shapes[0].touchedGoal:
        return False
    else:
        return True


# ----- Main game functions ---------------------

def createHandlers():
    handler_P1_Wall = space.add_collision_handler(COL_PLAYER1, COL_WALL)
    handler_P1_Wall.begin = begin_PlayerWall
    handler_P1_Wall.separate = separate_PlayerWall

    handler_P2_Wall = space.add_collision_handler(COL_PLAYER2, COL_WALL)
    handler_P2_Wall.begin = begin_PlayerWall
    handler_P2_Wall.separate = separate_PlayerWall


    handler_Ball_Goal = space.add_collision_handler(COL_BALL, COL_GOAL)
    handler_Ball_Goal.begin = begin_BallGoal

    handler_Ball_Wall = space.add_collision_handler(COL_BALL, COL_WALL)
    handler_Ball_Wall.begin = begin_BallWall

    handler_Ball_Player1 = space.add_collision_handler(COL_BALL, COL_PLAYER1)
    handler_Ball_Player1.begin = begin_BallPlayer

    handler_Ball_Player2 = space.add_collision_handler(COL_BALL, COL_PLAYER1)
    handler_Ball_Player2.begin = begin_BallPlayer

def resetBall():
    # reset ball's position to middle of field
    # and velocity is random
    ball.body.position = MIDX, MIDY
    ball.body.velocity = random.randint(-300,300), random.randint(-300,300)

    if ball.body.velocity.length < 300:
        ball.body.velocity = ball.body.velocity.scale_to_length(300)
    if ball.body.velocity[1] < 100:
        ball.body.velocity = ball.body.velocity[0], ball.body.velocity[1] + 100

    ball.shape.touchedGoal = False


def handleInput(player: Player):

    pVel = player.body.velocity
    pid = player.shape.id
    keys = pg.key.get_pressed()

    dir = ""

    if (keys[pg.K_a] and pid == 1) or (keys[pg.K_LEFT] and pid == 2):
        #dir += "L"

        # TODO: make this change columns
        pass
    if (keys[pg.K_d] and pid == 1) or (keys[pg.K_RIGHT] and pid == 2):
        #dir += "R"

        # TODO: make this change columns
        pass
    if (keys[pg.K_w] and pid == 1) or (keys[pg.K_UP] and pid == 2):
        dir += "U"
    if (keys[pg.K_s] and pid == 1) or (keys[pg.K_DOWN] and pid == 2):
        dir += "D"


    if dir in ["U","LRU"]:
        # player.body.angle = mth.radians(90)
        # player.angle = 90
        if not player.touchU:
            pVel = 0,-P_SPEED
        else:
            pVel = 0,0

    if dir in ["D","LRD"]:
        # player.body.angle = mth.radians(-90)
        # player.angle = -90
        if not player.touchD:
            pVel = 0,P_SPEED
        else:
            pVel = 0,0


    if dir in ["","LR","UD","LRUD"]:
        pVel = 0,0

    # speed up
    if ((keys[pg.K_SPACE] and pid == 1) or (keys[pg.K_RCTRL] and pid == 2)) and (player.stamina >= 0):
        player.fast = True
        player.heldFast = True
    else:
        if not keys[pg.K_SPACE]:
            player.heldFast = False
        player.fast = False

    if player.fast:
        pVel = pVel[0] * P_SPEED_MULTIPLIER, pVel[1] * P_SPEED_MULTIPLIER
        player.stamina -= SPEND_STAMINA

    # set player's velocity
    player.body.velocity = pVel


def update():
    pGroup.update()
    ball.update()
    timer.update()

def draw():
    screen.fill(GREEN)
    screen.blit(BG, (0,80))

    ball.draw()

    for sprite in pGroup.sprites():
        sprite.draw()

    for goal in goalGroup.sprites():
        goal.draw()

    for wall in wallList:
        wall.draw()

    score.draw()

    pg.display.update()





def main():
    run = True
    clock = pg.time.Clock()

    createHandlers()

    while run:
        space.step(1/FPS)
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run = False
                break
            if event.type == EVENT_RESET or (event.type == pg.KEYDOWN and event.key == pg.K_r):
                resetBall()
            

        for sprite in pGroup.sprites():
            handleInput(sprite)

        update()
        draw()

    pg.quit()


if __name__ == '__main__':
    main()