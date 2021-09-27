from Objects.Team import Team
from Objects.Player import *
from Objects.Ball import *
from Objects.Field import *
from Objects.Score import *


# ------ Game global variables -----------------------------

# NOTE: Passing in (x,y) coordinates in pm.Space() <=> (0,0) is bottom left
# So Pymunk's physics are upside down, but Pygame still blits it correctly

def randomBallVel() -> tuple:
    x = rd.choice([rd.randint(-300,-100), rd.randint(100,300)])
    y = rd.choice([rd.randint(-300,-100), rd.randint(100,300)])
    return (x,y)


ball = Ball(MIDX, MIDY, randomBallVel())

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

    def update(self):
        if self.timer:
            self.timer -= 1
        elif self.timer == 0 and ball.shape.touchedGoal:
            pg.event.post(pg.event.Event(EVENT_RESET))

timer = Timer()



# ----- CollisionHandler functions ---------------------------------------------------


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
    arbiter.shapes[0].body.velocity = arbiter.shapes[0].body.velocity.scale_to_length(52)

    if arbiter.shapes[1].id == 1:
        score.score_P2 += 1
    else:
        score.score_P1 += 1
    
    GOAL.play()
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

def begin_BallPlayer(arbiter, space, data) -> bool:
    if arbiter.shapes[0].touchedGoal:
        return False
    else:
        return True


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


    handler_Ball_Player13 = space.add_collision_handler(COL_BALL, COL_PLAYER13)
    handler_Ball_Player13.begin = begin_BallPlayer

    handler_Ball_Player23 = space.add_collision_handler(COL_BALL, COL_PLAYER23)
    handler_Ball_Player23.begin = begin_BallPlayer


def resetBall():
    # reset ball's position to middle of field
    # and velocity is random
    ball.body.position = MIDX, MIDY
    ball.body.velocity = randomBallVel()

    if ball.body.velocity.length < 300:
        ball.body.velocity = ball.body.velocity.scale_to_length(300)

    ball.shape.touchedGoal = False




def update():
    team1.update()
    team2.update()
    ball.update()
    timer.update()

def update_AI():
    # TODO: AI version of game

    team1.update()
    #team2.update()
    
    ball.update()
    timer.update()

def drawDash():
    curCol1 = team1.column[team1.curColumnTarget]
    dashSize1 = DASH_BLUE.get_width(), P1.get_height() + 20
    scaledDash1 = pg.transform.scale(DASH_BLUE, dashSize1)
    for player1 in curCol1.sprites():
        if player1.fast:
            if player1.body.velocity[1] < 0:
                screen.blit(scaledDash1, (player1.body.position[0] - P1_R, player1.body.position[1]))
            else:
                scaledDash1 = pg.transform.flip(scaledDash1, 0, 1)
                screen.blit(scaledDash1, (player1.body.position[0] - P1_R, player1.body.position[1] - P1.get_height() - 20))

    curCol2 = team2.column[team2.curColumnTarget]
    dashSize2 = DASH_RED.get_width(), P2.get_height() + 20
    scaledDash2 = pg.transform.scale(DASH_RED, dashSize2)
    for player2 in curCol2.sprites():
        if player2.fast:
            if player2.body.velocity[1] < 0:
                screen.blit(scaledDash2, (player2.body.position[0] - P2_R, player2.body.position[1]))
            else:
                scaledDash2 = pg.transform.flip(scaledDash2, 0, 1)
                screen.blit(scaledDash2, (player2.body.position[0] - P2_R, player2.body.position[1] - P2.get_height() - 20))


def draw():
    screen.fill(DARKGREEN)
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

    drawDash()
    
    for group in listGroup:
        for player in group.sprites():
            player.draw()

    score.draw()

    pg.display.update()



# ----- Game states -----------------------------------------------------------------------



def main2P():
    run = True
    clock = pg.time.Clock()

    createHandlers()

    while run:
        space.step(1/FPS)
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                run = False
                score.reset()
                resetBall()
                break
            if event.type == EVENT_RESET or (event.type == pg.KEYDOWN and event.key == pg.K_r):
                resetBall()
        # for sprite in pGroup.sprites():
        #     handleInput(sprite)
        if not run:
            break

        update()
        draw()

def mainAI():
    run = True
    clock = pg.time.Clock()

    createHandlers()

    while run:
        space.step(1/FPS)
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                run = False
                score.reset()
                resetBall()
                break
            if event.type == EVENT_RESET or (event.type == pg.KEYDOWN and event.key == pg.K_r):
                resetBall()
        # for sprite in pGroup.sprites():
        #     handleInput(sprite)

        if not run:
            break

        update_AI()
        draw()    


def menu():
    run = True
    clock = pg.time.Clock()

    button_2P = pg.Rect(100, 300, 180, 80)
    button_AI = pg.Rect(100, 400, 180, 80)
    btnList = [button_2P, button_AI]

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run = False
                break
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mPos = pg.mouse.get_pos()
                if button_2P.collidepoint(mPos):
                    main2P()
                elif button_AI.collidepoint(mPos):
                    mainAI()
        
        draw_menu(btnList)

    pg.quit()


def draw_menu(btnList: List[pg.Rect]):
    screen.fill(BLACK)
    screen.blit(MENU_BG, (0,0))

    # Draw title
    txtSurf = TITLE_FONT.render("Tiny Football", 1, BLACK)
    txtRect = pg.Rect(0,0, txtSurf.get_width(), txtSurf.get_height())
    pg.draw.rect(screen, BLACK, pg.Rect(40, 50, txtRect.width + 60, txtRect.height + 50))
    pg.draw.rect(screen, WHITE, pg.Rect(50, 60, txtRect.width + 40, txtRect.height + 30))
    screen.blit(txtSurf, (70, 70))


    # Draw 2P button
    button2PSurf = BUTTON_FONT.render("2-Player", 1, BLACK)
    pg.draw.rect(screen, GRAY, btnList[0])
    screen.blit(button2PSurf, (btnList[0].x + 15, btnList[0].y + 15))

    # Draw vs AI button
    button2PSurf = BUTTON_FONT.render("Vs. AI", 1, BLACK)
    pg.draw.rect(screen, GRAY, btnList[1])
    screen.blit(button2PSurf, (btnList[1].x + 15, btnList[1].y + 15))

    pg.display.update()




if __name__ == '__main__':
    menu()