from Objects.Team import Team
from Objects.Player import *
from Objects.Ball import *
from Objects.Field import *
from Objects.Score import *


# ------ Game global variables -----------------------------

# NOTE: Passing in (x,y) coordinates in pm.Space() <=> (0,0) is bottom left
# So Pymunk's physics are upside down, but Pygame still blits it correctly

ball = Ball(MIDX, MIDY, B_VEL)

score = ScoreController()

"""
    Layout: 
            50   150  250  350  450  550  650  750  -> (x)
            1A - 2A - 3B - 5A - 5B - 3A - 2B - 1B
"""

p1_1  = Player(50, MIDY, 1, COL_PLAYER13)
p1_21 = Player(150, MIDY - 50, 1, COL_PLAYER12)
p1_22 = Player(150, MIDY + 50, 1, COL_PLAYER12)
p1_41 = Player(350, MIDY - 200, 1, COL_PLAYER11)
p1_42 = Player(350, MIDY - 100, 1, COL_PLAYER11)
p1_43 = Player(350, MIDY, 1, COL_PLAYER11)
p1_44 = Player(350, MIDY + 100, 1, COL_PLAYER11)
p1_45 = Player(350, MIDY + 200, 1, COL_PLAYER11)
p1_61 = Player(550, MIDY - 120, 1, COL_PLAYER10)
p1_62 = Player(550, MIDY, 1, COL_PLAYER10)
p1_63 = Player(550, MIDY + 120, 1, COL_PLAYER10)

p2_1  = Player(WIDTH - 50, MIDY, 2, COL_PLAYER23)
p2_21 = Player(WIDTH - 150, MIDY - 50, 2, COL_PLAYER22)
p2_22 = Player(WIDTH - 150, MIDY + 50, 2, COL_PLAYER22)
p2_41 = Player(WIDTH - 350, MIDY - 200, 2, COL_PLAYER21)
p2_42 = Player(WIDTH - 350, MIDY - 100, 2, COL_PLAYER21)
p2_43 = Player(WIDTH - 350, MIDY, 2, COL_PLAYER21)
p2_44 = Player(WIDTH - 350, MIDY + 100, 2, COL_PLAYER21)
p2_45 = Player(WIDTH - 350, MIDY + 200, 2, COL_PLAYER21)
p2_61 = Player(WIDTH - 550, MIDY - 120, 2, COL_PLAYER20)
p2_62 = Player(WIDTH - 550, MIDY, 2, COL_PLAYER20)
p2_63 = Player(WIDTH - 550, MIDY + 120, 2, COL_PLAYER20)


wallL = Wall((BORDER, BORDER + MENU_HEIGHT), (BORDER, HEIGHT - BORDER), 1)
wallR = Wall((WIDTH - BORDER, BORDER + MENU_HEIGHT), (WIDTH - BORDER, HEIGHT - BORDER), 2)
wallU = Wall((BORDER, BORDER + MENU_HEIGHT), (WIDTH - BORDER, BORDER + MENU_HEIGHT), 3)
wallD = Wall((BORDER, HEIGHT - BORDER), (WIDTH - BORDER, HEIGHT - BORDER), 4)

goal1 = Goal((BORDER + 5, MIDY - 80), (BORDER + 5, MIDY + 80), 1)
goal2 = Goal((WIDTH - BORDER - 5, MIDY - 80), (WIDTH - BORDER - 5, MIDY + 80), 2)


pGroup10 = pg.sprite.Group(p1_61, p1_62, p1_63)
pGroup11 = pg.sprite.Group(p1_41, p1_42, p1_43, p1_44, p1_45)
pGroup12 = pg.sprite.Group(p1_21, p1_22)
pGroup13 = pg.sprite.Group(p1_1)

pGroup20 = pg.sprite.Group(p2_61, p2_62, p2_63)
pGroup21 = pg.sprite.Group(p2_41, p2_42, p2_43, p2_44, p2_45)
pGroup22 = pg.sprite.Group(p2_21, p2_22)
pGroup23 = pg.sprite.Group(p2_1)

listGroup = [pGroup10, pGroup11, pGroup12, pGroup13, pGroup20, pGroup21, pGroup22, pGroup23]

team1 = Team(screen, pGroup10, pGroup11, pGroup12, pGroup13, Player1Keys)
team2 = Team(screen, pGroup20, pGroup21, pGroup22, pGroup23, Player2Keys)

goalGroup = pg.sprite.Group(goal1, goal2)
wallList = [wallL, wallR, wallU, wallD]


# ----- Timer -------------------------------------

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

def getGroupIdxByCollistionType(col_type):
    if col_type == COL_PLAYER10:
        return 0
    elif col_type == COL_PLAYER11:
        return 1
    elif col_type == COL_PLAYER12:
        return 2
    elif col_type == COL_PLAYER13:
        return 3
    elif col_type == COL_PLAYER20:
        return 4
    elif col_type == COL_PLAYER21:
        return 5
    elif col_type == COL_PLAYER22:
        return 6
    elif col_type == COL_PLAYER23:
        return 7

def begin_PlayerWall(arbiter, space, data) -> bool:
    col_type = arbiter.shapes[0].collision_type
    idx = getGroupIdxByCollistionType(col_type)
    

    wall = arbiter.shapes[1].id
    pid = arbiter.shapes[0].id

    for player in listGroup[idx]:    
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
    col_type = arbiter.shapes[0].collision_type
    idx = getGroupIdxByCollistionType(col_type)

    wall = arbiter.shapes[1].id
    pid = arbiter.shapes[0].id

    for player in listGroup[idx]:
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
        BOUNCE.play()
        return True


# def begin_BallPlayer(arbiter, space, data) -> bool:
#     if arbiter.shapes[0].touchedGoal:
#         return False
#     else:
#         return True



# ----- Main game functions ---------------------

def createHandlers():
    handler_P10_Wall = space.add_collision_handler(COL_PLAYER10, COL_WALL)
    handler_P10_Wall.begin = begin_PlayerWall
    handler_P10_Wall.separate = separate_PlayerWall

    handler_P11_Wall = space.add_collision_handler(COL_PLAYER11, COL_WALL)
    handler_P11_Wall.begin = begin_PlayerWall
    handler_P11_Wall.separate = separate_PlayerWall

    handler_P12_Wall = space.add_collision_handler(COL_PLAYER12, COL_WALL)
    handler_P12_Wall.begin = begin_PlayerWall
    handler_P12_Wall.separate = separate_PlayerWall

    handler_P13_Wall = space.add_collision_handler(COL_PLAYER13, COL_WALL)
    handler_P13_Wall.begin = begin_PlayerWall
    handler_P13_Wall.separate = separate_PlayerWall

    handler_P20_Wall = space.add_collision_handler(COL_PLAYER20, COL_WALL)
    handler_P20_Wall.begin = begin_PlayerWall
    handler_P20_Wall.separate = separate_PlayerWall

    handler_P21_Wall = space.add_collision_handler(COL_PLAYER21, COL_WALL)
    handler_P21_Wall.begin = begin_PlayerWall
    handler_P21_Wall.separate = separate_PlayerWall

    handler_P22_Wall = space.add_collision_handler(COL_PLAYER22, COL_WALL)
    handler_P22_Wall.begin = begin_PlayerWall
    handler_P22_Wall.separate = separate_PlayerWall

    handler_P23_Wall = space.add_collision_handler(COL_PLAYER23, COL_WALL)
    handler_P23_Wall.begin = begin_PlayerWall
    handler_P23_Wall.separate = separate_PlayerWall

    handler_Ball_Goal = space.add_collision_handler(COL_BALL, COL_GOAL)
    handler_Ball_Goal.begin = begin_BallGoal

    handler_Ball_Wall = space.add_collision_handler(COL_BALL, COL_WALL)
    handler_Ball_Wall.begin = begin_BallWall

    # handler_Ball_Player1 = space.add_collision_handler(COL_BALL, COL_PLAYER1)
    # handler_Ball_Player1.begin = begin_BallPlayer

    # handler_Ball_Player2 = space.add_collision_handler(COL_BALL, COL_PLAYER1)
    # handler_Ball_Player2.begin = begin_BallPlayer

def resetBall():
    # reset ball's position to middle of field
    # and velocity is random
    ball.body.position = MIDX, MIDY
    ball.body.velocity = random.randint(-300,300), random.randint(-300,300)

    if ball.body.velocity.length < 300:
        ball.body.velocity = ball.body.velocity.scale_to_length(300)
    if abs(ball.body.velocity[0]) < 100:
        ball.body.velocity = 100, ball.body.velocity[1]

    ball.shape.touchedGoal = False


def handleInput(player: Player):

    pVel = player.body.velocity
    pid = player.shape.id
    keys = pg.key.get_pressed()

    dir = ""

    # TODO: make this change columns
    if (keys[pg.K_a] and pid == 1) or (keys[pg.K_LEFT] and pid == 2):
        pass
    if (keys[pg.K_d] and pid == 1) or (keys[pg.K_RIGHT] and pid == 2):
        pass

    if (keys[pg.K_w] and pid == 1) or (keys[pg.K_UP] and pid == 2):
        dir += "U"
        if not player.touchU:
            pVel = 0,-P_SPEED
        else:
            pVel = 0,0
    if (keys[pg.K_s] and pid == 1) or (keys[pg.K_DOWN] and pid == 2):
        dir += "D"
        if not player.touchD:
            pVel = 0,P_SPEED
        else:
            pVel = 0,0

    if dir in ["","UD"]:
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
    team1.update()
    team2.update()
    ball.update()
    timer.update()

def draw():
    screen.fill(GREEN)
    screen.blit(BG, (0,80))

    ball.draw()

    for goal in goalGroup.sprites():
        goal.draw()

    for wall in wallList:
        wall.draw()

    team1.draw()
    team2.draw()
    # for player in pGroup.sprites():
    #     pg.draw.line(screen, BROWN, (player.body.position[0], MENU_HEIGHT), (player.body.position[0], HEIGHT), 1)

    # for player in pGroup.sprites():
    #     player.draw()
    for group in listGroup:
        for player in group.sprites():
            player.draw()

    score.draw()

    pg.display.update()

# ----- Game states -----------------------------------------------

state = 'menu'

def gameStateManager():
    pg.init()
    execute = True
    while execute:
        if state == 'menu':
            menu()
        elif state == '2P':
            main2P()
        elif state == 'quit':
            execute = False
            
    pg.quit()


class IntWrapper:
    def __init__(self, num):
        self.num = num

def update_menu(num: IntWrapper):
    num.num += 1

def draw_menu(num: IntWrapper):
    screen.fill(BLACK)

    txtSurf = FONT.render(str(num.num), 1, WHITE)
    screen.blit(txtSurf, (50,50))

    pg.display.update()




def menu():
    run = True
    clock = pg.time.Clock()
    num = IntWrapper(0)

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                global state
                state = 'quit'
                return
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                global state
                state = '2P'
                return
        
        update_menu(num)
        draw_menu(num)
        

    pg.quit()

# -------------

def main2P():
    run = True
    clock = pg.time.Clock()

    createHandlers()

    while run:
        space.step(1/FPS)
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run = False
                global state
                state = 'menu'
                break
            if event.type == EVENT_RESET or (event.type == pg.KEYDOWN and event.key == pg.K_r):
                resetBall()
            

        # for sprite in pGroup.sprites():
        #     handleInput(sprite)

        update()
        draw()



if __name__ == '__main__':
    while True:
        gameStateManager()