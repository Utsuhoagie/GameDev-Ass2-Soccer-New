from Imports.Mid import *

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
