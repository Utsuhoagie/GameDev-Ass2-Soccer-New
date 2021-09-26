<<<<<<< HEAD
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
=======
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
>>>>>>> a4fd22820385f59bd6c9bf2a4186fe443f3b9862
wallList = [wallL, wallR, wallU, wallD]