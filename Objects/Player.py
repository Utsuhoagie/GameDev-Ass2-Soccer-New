from Init import *


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, id: int, collision_type):
        super().__init__()
        self.body = pm.Body(body_type = pm.Body.KINEMATIC)
        self.body.position = x, y

        self.shape = pm.Circle(self.body, P1_R)
        self.shape.elasticity = 1
        

        if id == 1:
            self.frames = [P1]    #, P1_CHARGE]
            self.shape.collision_type = collision_type
        elif id == 2:
            self.frames = [P2]   #, P2_CHARGE]
            self.shape.collision_type = collision_type

        self.shape.id = id

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
        self._handleInput()

        # Heal stamina after releasing Space
        if not self.heldFast and not self.fast and self.stamina < MAX_STAMINA:
            self.stamina += HEAL_STAMINA


    def draw(self):
        blitPos = self.body.position[0] - self.image.get_width()//2, self.body.position[1] - self.image.get_height()//2

        screen.blit(self.image, blitPos)

    def setZeroVelocity(self):
        self.body.velocity = (0, 0)

    def _handleInput(self):

        pVel = self.body.velocity
        pid = self.shape.id
        keys = pg.key.get_pressed()

        dir = ""

        if (keys[pg.K_w] and pid == 1) or (keys[pg.K_UP] and pid == 2):
            dir += "U"
            if not self.touchU:
                pVel = 0,-P_SPEED
            else:
                pVel = 0,0
        if (keys[pg.K_s] and pid == 1) or (keys[pg.K_DOWN] and pid == 2):
            dir += "D"
            if not self.touchD:
                pVel = 0,P_SPEED
            else:
                pVel = 0,0

        if dir in ["","UD"]:
            pVel = 0,0


        # speed up
        if ((keys[pg.K_SPACE] and pid == 1) or (keys[pg.K_RCTRL] and pid == 2)) and (self.stamina >= 0) and pVel != (0,0):
            self.fast = True
            self.heldFast = True
        else:
            if (not keys[pg.K_SPACE] and pid == 1) or (not keys[pg.K_RCTRL] and pid == 2):
                self.heldFast = False
            self.fast = False

        if self.fast:
            pVel = pVel[0] * P_SPEED_MULTIPLIER, pVel[1] * P_SPEED_MULTIPLIER
            self.stamina -= SPEND_STAMINA


        # set player's velocity
        self.body.velocity = pVel
