from TimerColHandlers import *


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